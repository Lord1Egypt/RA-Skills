import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { writeOutputFile } from "../utils/output.js";

const execFileAsync = promisify(execFile);

export async function sendEmail({
  mode = "file",
  emailMessage,
  outPath = null,
  sendmailPath = "sendmail",
  to = null,
  subject = null,
  textBody = null,
  htmlBody = null,
  nexlinkCliPath = null,
  pythonBin = "python3",
  env = undefined,
}) {
  if (mode === "file") {
    if (!outPath) {
      throw new Error("Email file delivery requires --email-out.");
    }

    await writeOutputFile(outPath, emailMessage);
    return { mode: "file", outPath };
  }

  if (mode === "sendmail") {
    await execFileAsync(sendmailPath, ["-t", "-i"], { input: emailMessage, env });
    return { mode: "sendmail" };
  }

  if (mode === "nexlink") {
    if (!nexlinkCliPath) {
      throw new Error("NexLink delivery requires --nexlink-cli pointing to nexlink.py.");
    }
    if (!to || !subject) {
      throw new Error("NexLink delivery requires recipient and subject.");
    }

    const body = htmlBody || textBody;
    if (!body) {
      throw new Error("NexLink delivery requires a body.");
    }

    const args = [nexlinkCliPath, "mail", "send", "--to", to, "--subject", subject, "--body", body];
    if (htmlBody) {
      args.push("--html");
    }

    await execFileAsync(pythonBin, args, { env });
    return { mode: "nexlink", cli: nexlinkCliPath };
  }

  throw new Error(`Unsupported email delivery mode: ${mode}`);
}
