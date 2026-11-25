# 第三方组件与资源声明

本仓库的代码和原创示例拟按根目录 [MIT License](LICENSE) 发布；**第三方程序和字体保留各自原许可证**，不随本项目 MIT 更改。此清单用于源码仓库审查；发布单文件 HTML 时，还须保证接收者能在发布物内直接查阅所需许可与署名，不能只把声明放在不随 HTML 一起发送的仓库里。

| 组件 / 资源 | 来源与用途 | 许可与附带文本 |
| --- | --- | --- |
| JSXGraph 1.14.3 | [官方仓库](https://github.com/jsxgraph/jsxgraph)，交互式几何 | 上游 `package.json` 声明 `(MIT OR LGPL-3.0-or-later)`；本项目按 MIT 选项使用。[MIT 全文](licenses/JSXGraph-LICENSE.MIT.txt)。[LGPL 全文](licenses/JSXGraph-LICENSE.LGPL.txt) 仅供参考。 |
| KaTeX 0.19.1 与其打包字体 | [官方仓库](https://github.com/KaTeX/KaTeX)，数学公式 | MIT。[KaTeX 许可全文](licenses/KaTeX-LICENSE.txt)。 |
| Latin Modern Roman 字体子集 | TeX Live 原始文件 `lmroman10-regular.otf`，仓库内 WOFF2 子集 | B. Jackowski 与 J. M. Nowacki 的 GUST Font License；须同时保留 [GUST Font License](licenses/GUST-FONT-LICENSE.TXT) 与所引的 [LPPL 1.3c](licenses/LPPL-1.3c.txt)。这**不是** SIL OFL。 |
| Noto Serif SC 字体子集 | [Noto CJK Serif](https://github.com/notofonts/noto-cjk/tree/main/Serif)，仓库内 WOFF2 子集 | 源字体元数据 © 2017–2023 Adobe；SIL Open Font License 1.1。[许可全文](licenses/Noto-Serif-SC-OFL-1.1.txt)。所用字体从原版裁字并转换格式，不再分发完整原文件。 |
| 折纸作品照片及手绘草图 | `examples/origami-ellipse/assets/`，课堂示例 | 项目原创素材，随本仓库许可发布。 |

项目自己的 `LICENSE` 仅覆盖有权许可的项目代码和原创素材，不覆盖以上字体和运行时依赖。字体子集并非通用字集：修改文字后应重新裁剪和复查许可证；对某份课件的发布物，也要重新检查其中实际使用的字体与其他第三方资源。
