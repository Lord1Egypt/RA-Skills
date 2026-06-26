import { execa } from "execa";

export async function sendMessage(target: string, text: string): Promise<void> {
  try {
    await execa("openclaw", ["message", "send", "--target", target, "--message", text]);
  } catch (err) {
    console.warn("[notify] openclaw message send failed:", err);
  }
}
