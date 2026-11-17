# Cron 配置模板

## 周内化 cron（每周日）

```
执行周内化任务。

遵循 learning-review skill 模式 B（周内化）：
1. 扫描本周 learning/notes/ 下的所有笔记
2. 读取对应的 learning/reviews/post-learning/ 复盘报告
3. 识别待内化项，执行内化（更新 AGENTS.md、TOOLS.md、SOUL.md、memory/）
4. 写内化报告到 learning/reviews/weekly/YYYY-Www.md

安静执行，不推群。
```

## 应用检查 cron（每两周）

```
执行应用检查任务。

遵循 learning-review skill 模式 C（应用检查）：
1. 读取最近 14 天的 memory 文件
2. 读取最近 14 天的学习笔记
3. 交叉比对：哪些学过的知识在日常工作中被应用了
4. 写应用检查报告到 learning/reviews/application/YYYY-MM-DD.md

安静执行，不推群。
```

## 压缩归档 cron（每月）

```
执行压缩归档任务。

遵循 learning-review skill 模式 D（压缩归档）：
1. 扫描 inline 文件（AGENTS.md, SOUL.md, MEMORY.md），检查是否超过 150 行
2. 识别可移出的内容：不需要每次对话看到的细节、已内化的知识、过时上下文
3. 将移出内容写入 references/<topic>.md
4. 在 inline 文件中替换为摘要 + 指针
5. 将不再需要的笔记从 learning/notes/ 移至 learning/archive/

安静执行，不推群。
```

## 知识落地 cron（每周，在周内化之后）

```
执行知识落地检查。

遵循 learning-review skill 模式 E（知识落地）：
1. 读取本周所有学习笔记和复盘报告
2. 对每条知识判断：能不能更新到 AGENTS.md 或某个 Skill 里
3. 能落地的：执行更新
4. 写知识落地报告到 learning/reviews/integration/YYYY-MM-DD.md

安静执行，不推群。
```
