// validate.js — 薄 CLI(保持旧用法/退出码/输出格式)
// 用法:
//   node validate.js slides/a.html slides/b.html ...
//   node validate.js slides/            (扫描目录下全部 .html,跳过 _ 开头的模板)
require("./validate/index.js").run(process.argv.slice(2));
