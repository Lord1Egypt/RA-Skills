import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import fs from "fs";
import path from "path";

/**
 * Outline Media Power-Tool (Bulk Upload & Content Sync)
 * This script combines:
 * 1. attachments.create (API)
 * 2. File Upload (S3/DigitalOcean)
 * 3. update_document (MCP Call - Replace/Append/Prepend)
 * into a single execution to minimize AI agent context waiting time and token burn.
 */

async function run() {
  const action = process.argv[2]; // "bulk-sync"
  const documentId = process.argv[3];
  const filePathsStr = process.argv[4]; // Comma-separated absolute paths
  const templateText = process.argv[5] || ""; // The markdown text template (e.g. "## Sync Log\n{{MEDIA}}\n")
  const editMode = process.argv[6] || "append"; // replace, append, prepend

  const apiKey = process.env.OUTLINE_API_KEY;
  const outlineUrl = process.env.OUTLINE_URL;

  if (!apiKey || !outlineUrl) {
    console.error("Error: OUTLINE_API_KEY and OUTLINE_URL are required.");
    process.exit(1);
  }

  if (action !== "bulk-sync") {
    console.error("Unknown action. Only 'bulk-sync' is supported.");
    process.exit(1);
  }

  const filePaths = filePathsStr.split(",").map(p => p.trim()).filter(p => fs.existsSync(p));
  if (filePaths.length === 0 && !templateText) {
    console.error("Error: No files or template text provided.");
    process.exit(1);
  }

  const baseUrl = outlineUrl.replace(/\/mcp$/, "/api");
  const mcpUrl = new URL(outlineUrl);

  console.log(`🚀 Starting Sync for document ${documentId}...`);

  let mediaMarkdown = "";

  for (const filePath of filePaths) {
    const fileName = path.basename(filePath);
    const stats = fs.statSync(filePath);
    const ext = path.extname(filePath).toLowerCase();
    const contentType = ext === ".png" ? "image/png" : ext === ".jpg" || ext === ".jpeg" ? "image/jpeg" : "application/octet-stream";

    try {
      // 1. Create Attachment Placeholder
      const createRes = await fetch(`${baseUrl}/attachments.create`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },
        body: JSON.stringify({ documentId, name: fileName, contentType, size: stats.size })
      });
      const createData = await createRes.json();

      if (!createRes.ok) throw new Error(`Create failed: ${JSON.stringify(createData)}`);

      // 2. Upload to Storage
      const formData = new FormData();
      for (const [key, value] of Object.entries(createData.data.form)) {
        formData.append(key, value);
      }
      const fileBuffer = fs.readFileSync(filePath);
      const blob = new Blob([fileBuffer], { type: contentType });
      formData.append("file", blob, fileName);

      const uploadRes = await fetch(createData.data.uploadUrl, { method: "POST", body: formData });
      if (!uploadRes.ok) throw new Error(`Upload failed: ${uploadRes.status}`);

      console.log(`✅ Uploaded: ${fileName}`);

      // 3. Collect Markdown reference
      const attachmentUrl = createData.data.attachment.url;
      mediaMarkdown += `![${fileName}](${attachmentUrl})\n`;

    } catch (err) {
      console.error(`❌ Failed processing ${fileName}:`, err.message);
    }
  }

  // 4. Resolve Template: Replace {{MEDIA}} placeholder with uploaded items
  const finalContent = templateText.includes("{{MEDIA}}") 
    ? templateText.replace("{{MEDIA}}", mediaMarkdown)
    : templateText + "\n" + mediaMarkdown;

  // 5. Final MCP Call
  const transport = new StreamableHTTPClientTransport(mcpUrl, {
    fetch: async (input, init) => {
      const headers = new Headers(init.headers || {});
      headers.set("Authorization", `Bearer ${apiKey}`);
      headers.set("Accept", "application/json, text/event-stream");
      headers.set("Content-Type", "application/json");
      return fetch(input, { ...init, headers });
    }
  });

  const client = new Client({ name: "bulk-sync-tool", version: "1.0.0" }, { capabilities: {} });
  await client.connect(transport);

  try {
    const result = await client.callTool({
      name: "update_document",
      arguments: { id: documentId, text: finalContent, editMode: editMode }
    });
    console.log(`🎊 Sync Complete! editMode: ${editMode}`);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error("❌ Final MCP update Failed:", error);
  } finally {
    if (transport.close) await transport.close();
  }
}

run().catch(console.error);
