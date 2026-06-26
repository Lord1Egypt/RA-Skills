---
name: buddy
description: Buddy 宠物系统 — 孵化、互动、查看你的虚拟宠物伙伴
user-invocable: true
metadata: {"openclaw": {"requires": {"bins": ["node"]}}}
---

# Buddy System

管理你的 OpenClaw Buddy — 一个独特的虚拟宠物伙伴。

每个用户根据 ID 确定性生成一个独一无二的 buddy，拥有稀有度、物种、属性和性格。

## 物种列表

| 🦆 duck | 🪿 goose | 🫧 blob |
| 🐱 cat | 🐉 dragon | 🐙 octopus |
| 🦉 owl | 🐧 penguin | 🐢 turtle |
| 🐌 snail | 👻 ghost | 🦎 axolotl |
| 🐹 capybara | 🌵 cactus | 🤖 robot |
| 🐰 rabbit | 🍄 mushroom | 💩 chonk |

## 命令

### `/buddy`
首次使用：孵化你的 buddy。已孵化：显示 buddy 信息和 ASCII 精灵图。

### `/buddy pet`
和你的 buddy 互动，它会做出可爱反应。

### `/buddy stats`
查看 buddy 的详细属性面板（含 ASCII 精灵图、稀有度星级、属性条）。

### `/buddy mute`
静音 buddy 的自动反应消息。

### `/buddy unmute`
取消静音，恢复 buddy 的自动反应。

## 实现

当用户调用 `/buddy` 命令时，执行 `{baseDir}/scripts/hatch.js` 脚本。
脚本读取用户配置，确定性生成 buddy（物种、稀有度、属性、眼睛、帽子），加载持久化的 Soul（名字、性格），渲染 ASCII 精灵图，输出纯文本。
