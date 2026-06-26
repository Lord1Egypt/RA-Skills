const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const scriptsDir = __dirname;
const generateScript = path.join(scriptsDir, "generate_contextweave.cjs");
const editScript = path.join(scriptsDir, "edit_contextweave.cjs");
const exportScript = path.join(scriptsDir, "export_contextweave_code.cjs");

const tempRequestFile = path.join(scriptsDir, "temp_e2e_request.md");
const testLinkPath = "/data/appdata/backend_service.py";

function runCmd(cmd) {
  console.log(`\n[RUNNING] ${cmd}`);
  const result = execSync(cmd, { encoding: "utf-8" });
  return result;
}

function parseJSONResult(output) {
  try {
    // Try parsing the whole output first
    return JSON.parse(output);
  } catch (e) {
    // If that fails, try to find a JSON block starting with { and ending with }
    const match = output.match(/\{[\s\S]*\}/);
    if (match) {
      try {
        return JSON.parse(match[0]);
      } catch (err) {
        throw new Error("Found {...} block but failed to parse as JSON");
      }
    }
    throw new Error("No JSON block found in output");
  }
}

async function main() {
  console.log("=== Starting E2E Link Test ===");

  // 1. Create a temporary input file
  const requestContent = `
# Request
Create a simple architecture with a Frontend node and a Backend node.

# CW
`;
  fs.writeFileSync(tempRequestFile, requestContent, "utf-8");
  console.log(`[SETUP] Created temp request file: ${tempRequestFile}`);

  let sessionId = null;
  try {
    // 2. Step 1: Generate structure
    const genCmd = `node "${generateScript}" --input_file "${tempRequestFile}"`;
    const genOutput = runCmd(genCmd);
    const genResult = parseJSONResult(genOutput);
    
    if (genResult.status !== "ok" || !genResult.session_id) {
      console.error("Generation failed:", genResult);
      process.exit(1);
    }
    sessionId = genResult.session_id;
    console.log(`[SUCCESS] Generated structure. Session ID: ${sessionId}`);

    // 3. Step 2: Edit to inject link
    const editRequest = `Add a link property '${testLinkPath}' to the Backend node`;
    const editCmd = `node "${editScript}" --session_id "${sessionId}" --user_request "${editRequest}"`;
    const editOutput = runCmd(editCmd);
    const editResult = parseJSONResult(editOutput);

    if (editResult.status !== "ok") {
      console.error("Edit failed:", editResult);
      process.exit(1);
    }
    console.log(`[SUCCESS] Edit command executed.`);

    // 4. Step 3: Export and Verify
    const exportPath = path.join(scriptsDir, "export_test_dir");
    const exportCmd = `node "${exportScript}" --session_id "${sessionId}" --path "${exportPath}"`;
    const exportOutput = runCmd(exportCmd);
    
    // Check if the link property exists in the exported cw file
    const exportedFile = path.join(exportPath, "diagram.cw");
    if (!fs.existsSync(exportedFile)) {
      console.error(`\n❌ E2E Test Failed! Exported file not found at ${exportedFile}`);
      process.exit(1);
    }
    
    const cwContent = fs.readFileSync(exportedFile, "utf-8");
    
    if (cwContent.includes(`link: ${testLinkPath}`) || cwContent.includes(`link: "${testLinkPath}"`) || cwContent.includes(`link: '${testLinkPath}'`)) {
      console.log(`\n======================================`);
      console.log(`✅ E2E Test Passed! Link was successfully injected.`);
      console.log(`======================================\n`);
    } else {
      console.error(`\n❌ E2E Test Failed! Link was not found in the exported code.`);
      console.log(`Exported Output:\n${cwContent}`);
      process.exit(1);
    }

  } catch (error) {
    console.error("Test execution failed:", error);
    process.exit(1);
  } finally {
    // Clean up
    if (fs.existsSync(tempRequestFile)) {
      fs.unlinkSync(tempRequestFile);
    }
    if (sessionId) {
      const cwFile = path.join(process.cwd(), `${sessionId}.cw`);
      if (fs.existsSync(cwFile)) {
        fs.unlinkSync(cwFile);
      }
    }
    const exportPath = path.join(scriptsDir, "export_test_dir");
    if (fs.existsSync(exportPath)) {
      const exportedFile = path.join(exportPath, "diagram.cw");
      if (fs.existsSync(exportedFile)) {
        fs.unlinkSync(exportedFile);
      }
      fs.rmdirSync(exportPath);
    }
  }
}

main();
