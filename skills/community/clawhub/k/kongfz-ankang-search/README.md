# 孔夫子安康文献检索技能

孔夫子旧书网拍卖栏目自动化检索技能，专注于陕西安康地区相关文献和书籍。

## 功能

- 自动搜索孔夫子拍卖栏目的安康相关拍品
- 固定搜索三个关键词：**安康**、**来鹿堂**、**兴安府**
- 发现相关拍品时自动汇总展示

## 触发方式

说出以下任一短语即可触发：

- "搜孔夫子拍卖安康"
- "孔夫子拍卖安康"  
- "搜孔夫子安康"

## 搜索关键词说明

| 关键词 | 说明 |
|--------|------|
| 安康 | 搜索安康地区相关文献和物品 |
| 来鹿堂 | 安康著名老字号（清代书商、印书局） |
| 兴安府 | 清代陕南行政区划（辖安康、汉阴、石泉等地） |

## 技术实现

使用 xbrowser 浏览器自动化访问孔夫子高级搜索页面：

```
https://search.kongfz.com/adv.html?type=pm
```

执行流程：打开页面 → 填入关键词 → 提交搜索 → 提取结果

## 文件结构

```
kongfz-ankang-search/
├── SKILL.md                          # 技能说明
├── README.md                         # 本文件
├── scripts/
│   └── kongfz_search_xbrowser.py     # 主检索脚本
└── references/
    ├── kongfz_structure.md           # 网站结构参考
    └── kongfz_actual_structure.md    # 实际结构说明
```

## 安装

### OpenClaw 用户

```bash
npx skills add <your-github-username>/kongfz-ankang-search -g
```

### 手动安装

将技能目录复制到 `~/.agents/skills/` 下即可。

## 依赖

- OpenClaw xbrowser 技能（浏览器自动化）

## 许可证

MIT
