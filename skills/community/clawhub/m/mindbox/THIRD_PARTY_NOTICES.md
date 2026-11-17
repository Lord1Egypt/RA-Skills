# Third-party notices

Mindbox code is MIT licensed; see [LICENSE](LICENSE). Bundled fonts retain their own SIL Open Font License 1.1 notices and reserved-name conditions. The code license does not replace those font licenses.

| Font | Local asset | License |
| --- | --- | --- |
| Noto Serif SC | `elegant.woff2` | `elegant-OFL.txt` |
| Noto Sans SC | `business.woff2` | `business-OFL.txt` |
| Ma Shan Zheng | `brush.woff2` | `brush-OFL.txt` |
| ZCOOL KuaiLe | `playful.woff2` | `playful-OFL.txt` |
| LXGW WenKai TC | `wenkai.woff2` | `wenkai-OFL.txt` |
| Inter | `inter.woff2` | `inter-OFL.txt` |
| Lora | `lora.woff2` | `lora-OFL.txt` |
| JetBrains Mono | `jetbrains.woff2` | `jetbrains-OFL.txt` |
| Excalifont | `excalifont.woff2` | `excalifont-OFL.txt` |

In the repository these files are in `assets/fonts/`; in an installed Skill they are in `assets/runtime/assets/fonts/`. `sources.json` in that directory records upstream locations and subset coverage. Standalone HTML embeds the used fonts and their license notices. Chinese subsets cover common characters; other characters fall back to system fonts, so uncommon glyphs can vary between computers.


The npx installer uses the MIT-licensed [Skills CLI](https://github.com/vercel-labs/skills) as a pinned npm dependency. Development tools and transitive licenses are recorded in `package-lock.json` and the installed packages. These npm dependencies are not bundled into, or needed by, the offline HTML or installed Skill runtime.
