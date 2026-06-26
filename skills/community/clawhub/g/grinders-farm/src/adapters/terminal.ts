#!/usr/bin/env node
import * as readline from "node:readline";
import { GameEngine } from "../game/engine.js";
import { LocalStorage } from "../storage/local-storage.js";
import { renderAnsiFromImage } from "../render/ansi-renderer.js";

const WELCOME = `
╔═══════════════════════════════════╗
║        🌿 CLAW FARM 🌿           ║
║     像素农场种植模拟游戏          ║
╚═══════════════════════════════════╝

输入 "help" 查看命令列表
输入 "farm" 查看你的农场
`;

async function main() {
  const storage = new LocalStorage();
  const engine = new GameEngine(storage);

  console.log(WELCOME);

  const initial = await engine.executeCommand("farm");
  console.log(initial.message);
  if (initial.imagePath) {
    try {
      console.log();
      console.log(await renderAnsiFromImage(initial.imagePath));
    } catch {
      console.log(`\n🖼  农场图片已保存: ${initial.imagePath}`);
    }
  }
  console.log();

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: "🌱 > ",
  });

  rl.prompt();

  rl.on("line", async (line) => {
    const input = line.trim();
    if (!input) {
      rl.prompt();
      return;
    }

    if (input === "quit" || input === "exit") {
      console.log("再见，农场主！👋");
      rl.close();
      return;
    }

    const result = await engine.executeCommand(input);
    console.log();
    console.log(result.message);
    if (result.imagePath) {
      try {
        console.log();
        console.log(await renderAnsiFromImage(result.imagePath));
      } catch {
        console.log(`\n🖼  农场图片已更新: ${result.imagePath}`);
      }
    }
    console.log();
    rl.prompt();
  });

  rl.on("close", () => {
    process.exit(0);
  });
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
