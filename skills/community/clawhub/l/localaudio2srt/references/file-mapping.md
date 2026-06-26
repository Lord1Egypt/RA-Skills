# File Mapping: references → TARGET_DIR

执行时按以下映射，将 `references/` 下的文件写入目标目录。

## 映射表

| references 源路径 | 目标路径（相对 TARGET_DIR） |
|-------------------|---------------------------|
| `references/package.json` | `package.json` |
| `references/tsconfig.json` | `tsconfig.json` |
| `references/tsconfig.node.json` | `tsconfig.node.json` |
| `references/vite.config.ts` | `vite.config.ts` |
| `references/tailwind.config.js` | `tailwind.config.js` |
| `references/postcss.config.js` | `postcss.config.js` |
| `references/index.html` | `index.html` |
| `references/.gitignore` | `.gitignore` |
| `references/LICENSE` | `LICENSE` |
| `references/start.sh` | `start.sh` |
| `references/requirements.txt` | `server/requirements.txt` |
| `references/transcribe_server.py` | `server/transcribe_server.py` |
| `references/src/App.tsx` | `src/App.tsx` |
| `references/src/main.tsx` | `src/main.tsx` |
| `references/src/index.css` | `src/index.css` |
| `references/src/types/index.ts` | `src/types/index.ts` |
| `references/src/utils/helpers.ts` | `src/utils/helpers.ts` |
| `references/src/store/queueStore.ts` | `src/store/queueStore.ts` |
| `references/src/components/DropZone.tsx` | `src/components/DropZone.tsx` |
| `references/src/components/FileCard.tsx` | `src/components/FileCard.tsx` |
| `references/src/components/FileList.tsx` | `src/components/FileList.tsx` |
| `references/src/components/Header.tsx` | `src/components/Header.tsx` |
| `references/src/components/ResultPanel.tsx` | `src/components/ResultPanel.tsx` |
| `references/src/components/SrtTranslatePage.tsx` | `src/components/SrtTranslatePage.tsx` |
| `references/src/components/StatsBar.tsx` | `src/components/StatsBar.tsx` |
| `references/src/components/TranscriptionSettings.tsx` | `src/components/TranscriptionSettings.tsx` |

## 额外需要创建的目录

- `models/` — 模型存放目录（gitignored，运行时由 start.sh 自动下载）

## 执行方式

1. 先创建目标目录和所有子目录：
   ```bash
   mkdir -p TARGET_DIR/{server,src/{components,store,types,utils},models}
   ```

2. 对每个映射项，使用 Read 工具读取 references 中的源文件，然后用 Write 工具写入目标路径

3. 写入 `start.sh` 后执行 `chmod +x TARGET_DIR/start.sh`

4. 全部文件写入后，按 SKILL.md 中的 Step 3~6 继续执行
