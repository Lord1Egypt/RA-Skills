#!/usr/bin/env node
import { GameEngine } from "../game/engine.js";
import { LocalStorage } from "../storage/local-storage.js";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

const storage = new LocalStorage();
const engine = new GameEngine(storage);
const IMAGE_SERVER_INFO_FILE = path.join(os.homedir(), ".grinders-farm", "image-server.json");

function resolveFarmImageUrl(imagePath: string): string {
  try {
    if (fs.existsSync(IMAGE_SERVER_INFO_FILE)) {
      const raw = JSON.parse(fs.readFileSync(IMAGE_SERVER_INFO_FILE, "utf8")) as { baseUrl?: unknown };
      if (typeof raw.baseUrl === "string" && raw.baseUrl.trim()) {
        const baseUrl = raw.baseUrl.trim().replace(/\/+$/, "");
        return `${baseUrl}/${encodeURIComponent(path.basename(imagePath))}`;
      }
    }
  } catch {
    // fall through to file:// fallback
  }
  return `file://${imagePath}`;
}

const command = process.argv.slice(2).join(" ");
if (!command) {
  console.log('Usage: npx tsx src/adapters/oneshot.ts <command>');
  console.log('Example: npx tsx src/adapters/oneshot.ts plant carrot A1');
  process.exit(1);
}

const result = await engine.executeCommand(command);
console.log(result.message);

if (result.imagePath) {
  console.log(`\n🖼 查看高清像素图: ${resolveFarmImageUrl(result.imagePath)}`);
}

process.exit(result.success ? 0 : 1);
