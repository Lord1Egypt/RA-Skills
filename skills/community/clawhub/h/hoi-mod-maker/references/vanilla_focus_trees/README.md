# 原版国策树参考库

> 收录 HOI4 全部 74 个国策树原始文本，供 modder 搜索 focus ID、参考布局结构和前置关系。
> 文件来源：游戏本体 `common/national_focus/` 目录。

## 快速使用

- **查 focus ID**：直接用编辑器在对应文件中搜索，或全局搜索整个文件夹
- **看布局结构**：搜索 `x =` / `y =` / `relative_position_id` / `inner_circle`
- **查前置关系**：搜索 `prerequisite` / `mutually_exclusive`
- **做 replace_path**：确认国策树 ID（下表 TreeID 列）

## 国策树索引

### 主要国家（独立完整树）

| 文件 | 国家 | Tree ID | 焦点数 | 视口 | 连续焦点 | 内圈 |
|------|------|---------|--------|------|---------|------|
| germany.txt | GER 德国 | `german_focus` | 437 | (0,76) | Y | 0 |
| japan.txt | JAP 日本 | `japan_wtt_focus` | 450 | - | Y | 0 |
| soviet.txt | SOV 苏联 | `soviet_focus` | 311 | - | Y | 0 |
| usa.txt | USA 美国 | `usa_focus` | 135 | - | Y | 0 |
| uk.txt | ENG 英国 | `british_focus` | 161 | - | - | 0 |
| france.txt | FRA 法国 | `french_focus` | 185 | - | - | 0 |
| italy.txt | ITA 意大利 | `italian_focus` | 314 | (0,0) | Y | 0 |
| poland.txt | POL 波兰 | `polish_focus` | 301 | - | - | 0 |
| china_nationalist.txt | CHI 国民中国 | `china_nationalist_focus` | 50 | - | Y | 0 |
| china_communist.txt | PRC 共产中国 | `china_communist_focus` | 43 | - | Y | 0 |
| manchukuo.txt | MAN 满洲国 | `manchukuo_focus` | 46 | - | Y | 0 |
| spain.txt | SPR 西班牙 | `spanish_focus` | 281 | (0,33) | Y | 0 |

### DLC: BftB 抵抗运动

| 文件 | 国家 | Tree ID | 焦点数 | 连续焦点 |
|------|------|---------|--------|---------|
| romania.txt | ROM 罗马尼亚 | `romanian_focus` | 92 | Y |
| yugoslavia.txt | YUG 南斯拉夫 | `yugoslavian_focus` | 118 | Y |
| hungary.txt | HUN 匈牙利 | `hungarian_focus` | 99 | Y |
| hungary_wuw.txt | HUN 匈牙利(文明冲突) | `wuw_hungarian_focus` | 238 | Y |
| czechoslovakia.txt | CZE 捷克 | `czech_focus` | 88 | Y |
| austria.txt | AUS 奥地利 | `austria_focus_tree` | 214 | Y |
| belgium.txt | BEL 比利时 | `belgium_focus` | 173 | Y |
| netherlands.txt | HOL 荷兰 | `netherlands_focus` | 137 | Y |

### DLC: BBA 发动全面战争

| 文件 | 国家 | Tree ID | 焦点数 | 连续焦点 |
|------|------|---------|--------|---------|
| turkey.txt | TUR 土耳其 | `turkish_focus` | 201 | Y |
| greece.txt | GRE 希腊 | `greek_focus` | 123 | Y |
| bulgaria.txt | BUL 保加利亚 | `bulgarian_focus` | 150 | Y |
| portugal.txt | POR 葡萄牙 | `portuguese_focus` | 122 | Y |
| ethiopia.txt | ETH 埃塞俄比亚 | `ethiopia_tree` | 204 | Y |

### DLC: NSB 摩托化部队

| 文件 | 国家 | Tree ID | 焦点数 | 连续焦点 |
|------|------|---------|--------|---------|
| estonia.txt | EST 爱沙尼亚 | `estonia_tree` | 59 | Y |
| latvia.txt | LAT 拉脱维亚 | `latvia_tree` | 56 | Y |
| lithuania.txt | LIT 立陶宛 | `lithuania_tree` | 86 | Y |

### DLC: AAT 大陆与非洲部队

| 文件 | 国家 | Tree ID | 焦点数 | 连续焦点 |
|------|------|---------|--------|---------|
| mexico.txt | MEX 墨西哥 | `mexico_focus_tree` | 114 | Y |
| brazil.txt | BRA 巴西 | `brazil_tree` | 170 | Y |
| argentina.txt | ARG 阿根廷 | `argentine_focus_tree` | 150 | Y |
| chile.txt | CHL 智利 | `chilean_focus_tree` | 205 | Y |
| afghanistan.txt | AFG 阿富汗 | `afghanistan_tree` | 201 | Y |
| iraq.txt | IRQ 伊拉克 | `iraq_focus` | 136 | Y |
| persia.txt | PER 波斯 | `persian_focus_tree` | 272 | Y |
| iceland.txt | ICE 冰岛 | `iceland_tree` | 89 | Y |
| switzerland.txt | SWI 瑞士 | `swiss_focus` | 160 | Y |
| norway.txt | NOR 挪威 | `norwegian_focus` | 192 | Y |
| sweden.txt | SWE 瑞典 | `sweden_focus` | 168 | Y |
| denmark.txt | DEN 丹麦 | `danish_focus` | 175 | Y |
| finland.txt | FIN 芬兰 | `finnish_focus` | 166 | Y |
| philippines.txt | PHI 菲律宾 | `philippines_focus` | 170 | Y |
| congo.txt | COG 刚果 | `congo_focus` | 152 | Y |
| paraguay.txt | PAR 巴拉圭 | `paraguay_focus` | 54 | Y |
| uruguay.txt | URY 乌拉圭 | `uruguay_focus` | 45 | Y |

### DLC: TSR 天佑君主（中国变体）

| 文件 | 国家 | Tree ID | 焦点数 |
|------|------|---------|--------|
| china_nationalist_warlord_TSR.txt | RNG 国民中国(军阀) | `china_nationalist_warlord_focus` | 78 |
| china_communist_warlord_TSR.txt | PRC 共产中国(军阀) | `china_communist_warlord_focus` | 41 |
| china_warlord.txt | YUN 军阀 | `china_warlord_focus` | 41 |
| china_warlord_sea.txt | YUN 军阀(海) | `china_warlord_sea_focus` | 155 |
| china_communist_sea.txt | PRC 共产中国(海) | `china_communist_focus_sea` | 203 |
| china_nationalist_sea.txt | CHI 国民中国(海) | `china_nationalist_sea_focus` | 275 |
| manchukuo_TSR.txt | MAN 满洲国(TSR) | `manchukuo_focus_tsr` | 87 |

### 英联邦国家

| 文件 | 国家 | Tree ID | 焦点数 | 连续焦点 |
|------|------|---------|--------|---------|
| india.txt | RAJ 英属印度 | `indian_focus` | 71 | - |
| india_goe.txt | RAJ 英属印度(GoE) | `indian_focus_goe` | 412 | Y |
| australia.txt | AST 澳大利亚 | `australian_focus` | 94 | Y |
| canada.txt | CAN 加拿大 | `canadian_focus` | 95 | - |
| south_africa.txt | SAF 南非 | `south_african_focus` | 80 | - |
| new_zealand.txt | NZL 新西兰 | `new_zealander_focus` | 59 | - |

### 特殊/衍生国家

| 文件 | 国家 | Tree ID | 焦点数 |
|------|------|---------|--------|
| free_france.txt | FRA 自由法国 | `free_french_focus` | 23 |
| vichy_france.txt | FRA 维希法国 | `vichy_french_focus` | 24 |

### 共享分支（Joint Branches）

| 文件 | 说明 |
|------|------|
| china_shared.txt | 中国共享分支 |
| china_shared_TSR.txt | 中国共享分支(TSR) |
| baltic_shared.txt | 波罗的海共享分支 |
| nordic_shared.txt | 北欧共享分支 |
| congo_shared.txt | 刚果共享分支 |
| goe_shared_saadabad_branch.txt | Saadabad 条约共享分支 |
| habsburg_joint.txt | 哈布斯堡联合分支 |
| horn_of_africa.txt | 非洲之角共享分支 |
| austro_hungarian_releasable_shared.txt | 奥匈释放国共享 |
| paraguay_uruguay_shared_branch.txt | 巴拉圭-乌拉圭共享 |
| ncns_ma_clique_joint_branch.txt | 马家军联合分支 |
| TSR_lingguang_incident_joint_branch.txt | 临光事件联合分支 |
| toa_shared_military_branch.txt | 大洋军事共享分支 |

### 通用树

| 文件 | Tree ID | 焦点数 |
|------|---------|--------|
| generic.txt | `generic_focus` | 56 |

## 文件说明

- `00_titlebar_styles.txt` — 标题栏样式定义，非国策树
- 视口位置 `?` 表示该树可能使用 `continuous_focus_position` 或动态计算，无固定 `initial_show_position`
- 连续焦点 `Y` 表示该国策树包含 `continuous_focus` 或连续焦点相关机制
