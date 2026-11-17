# Board maintenance source

本目录只保存 Board 的 React/JSX 维护源码，不是交付 framework，也不能被生成任务复制。

- 入口：`bridge-entry.jsx`
- React 维护源码：`react-source/`
- 画板界面文案：`react-source/board/i18n/`（`zh-CN` / `zh-TW` / `en` 字典与 locale 解析）
- 编译产物：`starter/framework/runtime/board.js`
- 其余交付 runtime、styles、vendor 与格式标识均直接维护在 `starter/framework/`

修改本目录后必须重新生成 `starter/framework/runtime/board.js`，运行 `node tools/check.mjs`，再通过 `file://` 回归 starter 和两个 demo。不得在仓库根目录恢复可运行的 `framework/`、`src/` 或 `index.html` 镜像。

重建 Board（维护机需要 esbuild）：

```sh
npx esbuild framework-source/bridge-entry.jsx \
  --bundle --minify --charset=utf8 \
  --outfile=starter/framework/runtime/board.js \
  --format=iife \
  --jsx=transform \
  --jsx-factory=React.createElement \
  --jsx-fragment=React.Fragment \
  --banner:js='/* PREBUILT VUE GLOBAL POC BOARD BRIDGE. BUSINESS SCREENS REQUIRE NO BUILD. */'
```
