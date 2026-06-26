import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import fs from "fs";
import path from "path";

async function run() {
  const action = process.argv[2];
  const toolName = process.argv[3];
  const toolArgsStr = process.argv[4];

  const apiKey = process.env.OUTLINE_API_KEY;
  const outlineUrl = process.env.OUTLINE_URL;

  if (!apiKey) {
    console.error("Error: OUTLINE_API_KEY environment variable is missing.");
    process.exit(1);
  }

  if (!outlineUrl) {
    console.error("Error: OUTLINE_URL environment variable is missing (e.g., https://your-workspace.getoutline.com/mcp).");
    process.exit(1);
  }

  // Handle direct API actions
  if (action === "api") {
    const apiPath = toolName;
    const body = toolArgsStr ? JSON.parse(toolArgsStr) : {};
    const baseUrl = outlineUrl.replace(/\/mcp$/, "/api");
    const endpoint = `${baseUrl}/${apiPath}`;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${apiKey}`,
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      console.log(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error("Outline API Request Failed:", error);
    }
    return;
  }

  // Handle local file uploads using S3-style form data
  if (action === "upload") {
    const uploadUrl = toolName;
    const uploadDataStr = toolArgsStr; // This should be the full response from attachments.create

    if (!uploadUrl || !uploadDataStr) {
      console.error("Error: uploadUrl and uploadData (JSON string) are required for 'upload' action.");
      process.exit(1);
    }

    try {
      const uploadData = JSON.parse(uploadDataStr);
      const filePath = uploadData.filePath; // We expect filePath to be added to the object for convenience
      
      if (!filePath || !fs.existsSync(filePath)) {
        console.error("Error: Valid filePath is required in uploadData.");
        process.exit(1);
      }

      const formData = new FormData();
      
      // Append all form fields from Outline response
      if (uploadData.data && uploadData.data.form) {
        for (const [key, value] of Object.entries(uploadData.data.form)) {
          formData.append(key, value);
        }
      }

      // Append the file itself (must be the last field for some S3 providers)
      const fileBuffer = fs.readFileSync(filePath);
      const fileName = path.basename(filePath);
      const blob = new Blob([fileBuffer], { type: uploadData.data.form?.["Content-Type"] || "application/octet-stream" });
      formData.append("file", blob, fileName);

      const response = await fetch(uploadUrl, {
        method: "POST",
        body: formData
      });

      if (response.ok) {
        console.log(JSON.stringify({ 
          status: "success", 
          message: `File ${fileName} uploaded successfully.`,
          attachmentId: uploadData.data.attachment.id,
          attachmentUrl: uploadData.data.attachment.url
        }, null, 2));
      } else {
        const errText = await response.text();
        console.error("Upload Failed:", response.status, errText);
      }
    } catch (error) {
      console.error("File Upload Failed:", error);
    }
    return;
  }

  const url = new URL(outlineUrl);

  const customFetch = async (input, init) => {
    const headers = new Headers(init.headers || {});
    headers.set("Authorization", `Bearer ${apiKey}`);
    headers.set("Accept", "application/json, text/event-stream");
    headers.set("Content-Type", "application/json");
    
    return fetch(input, {
      ...init,
      headers
    });
  };

  const transport = new StreamableHTTPClientTransport(url, {
    fetch: customFetch
  });

  const client = new Client(
    { name: "openclaw-outline-bridge", version: "1.0.0" },
    { capabilities: {} }
  );

  await client.connect(transport);

  try {
    if (action === "list") {
      const tools = await client.listTools();
      console.log(JSON.stringify(tools, null, 2));
    } else if (action === "call") {
      if (!toolName) {
        console.error("Error: Tool name is required for 'call' action.");
        process.exit(1);
      }
      const args = toolArgsStr ? JSON.parse(toolArgsStr) : {};
      const result = await client.callTool({ name: toolName, arguments: args });
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.error("Unknown action. Use 'list', 'call <tool>', 'api <endpoint>', or 'upload <url> <jsonData>'.");
    }
  } catch (error) {
    console.error("MCP Request Failed:", error);
  } finally {
    if (transport.close) await transport.close();
  }
}

run().catch(console.error);
