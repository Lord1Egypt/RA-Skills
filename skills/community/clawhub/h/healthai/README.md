# 健康管理技能 (Health Management Skill) - 安装说明

## 📦 技能简介

通用健康管理流程封装，支持：
- 📊 体检报告解读
- 🍽️ 饮食方案生成
- 🏃 运动计划制定
- 📋 跟踪管理表生成
- 📱 **腾讯文档在线同步**（微信直接访问）
- ⏰ 定时打卡提醒
- 🔥 卡路里计算

## 📁 文件结构

```
HealthSkill/
├── SKILL.md                          # 技能描述文件
├── README.md                         # 本安装说明
├── templates/
│   ├── 健康管理方案模板.md           # 方案文档模板
│   ├── 健康跟踪表模板.mdx           # 腾讯文档MDX模板
│   └── health_tracking_generator.py  # Excel生成脚本
├── scripts/
│   ├── calorie_calc.py               # 卡路里计算脚本
│   ├── create_online_doc.py          # 腾讯文档创建脚本
│   └── update_record.py              # 打卡记录更新脚本
└── references/
    ├── 指标参考范围.md               # 医学指标参考
    └── 卡路里计算参考.md             # 运动消耗参考
```

## 🚀 安装方法

### 方法1：复制到用户Skills目录

```bash
# 复制到用户skills目录
cp -r ~/Downloads/HealthSkill ~/.workbuddy/skills/

# 验证安装
ls ~/.workbuddy/skills/HealthSkill/
```

### 方法2：复制到项目Skills目录

```bash
cp -r ~/Downloads/HealthSkill /path/to/project/.workbuddy/skills/
```

## ⚙️ 腾讯文档配置

### 获取Token

1. 访问 [https://docs.qq.com/open/auth/mcp.html](https://docs.qq.com/open/auth/mcp.html)
2. 点击"获取授权码"
3. 复制Token

### 配置环境变量

```bash
export TENCENT_DOCS_TOKEN="你的Token值"
```

### 验证配置

```bash
mcporter list | grep tencent-docs
```

## 📖 使用方式

### 方式1：通过AI对话（推荐）

直接描述需求：
```
帮我制定健康管理方案
- 年龄34岁，男性
- 身高175cm，体重71kg
- 饮食习惯：蛋奶素
- 运动时间：中午
- 体检异常：ALT 50.65偏高

记录今天步数：10698步

创建腾讯文档健康跟踪表
```

### 方式2：使用命令行脚本

```bash
# 计算卡路里
python scripts/calorie_calc.py --steps 10698 --weight 70.9 --age 34

# 创建腾讯文档
python scripts/create_online_doc.py --title "我的健康跟踪表"

# 更新打卡记录
python scripts/update_record.py --file-id 文档ID --steps 10698 --weight 70.9
```

### 方式3：生成Excel

```bash
# 安装依赖
pip install openpyxl

# 生成跟踪表
python templates/health_tracking_generator.py --output 健康管理.xlsx --diet 蛋奶素
```

## 📱 腾讯文档使用

### 创建在线文档

腾讯文档支持微信直接访问，适合：
- ✅ 实时同步（多设备）
- ✅ 微信直接查看
- ✅ 分享给家人/教练
- ✅ 无需下载App

### 分享设置

1. 打开文档链接
2. 点击右上角「...」
3. 选择「分享」
4. 生成邀请链接
5. 选择权限（查看/编辑）
6. 发送给对方

### 微信访问

文档链接格式：`https://docs.qq.com/aio/文档ID`

微信内直接点击链接即可打开查看和编辑。

## 🔥 卡路里计算

### 使用示例

```bash
python scripts/calorie_calc.py --steps 10698 --weight 70.9 --age 34

# 输出：
# 📊 运动数据：
#    步数：10,698步
#    距离：约8km
#    时长：约70分钟
# 🔥 卡路里消耗：
#    总计：约 740 卡
```

### 计算公式

```
有效减脂心率 = (220 - 年龄) × 60%~70%

例：34岁 → 112~130 次/分
```

## ⚠️ 注意事项

1. **本方案仅供参考**，具体治疗建议请遵医嘱
2. 如有严重健康问题，请先咨询专业医生
3. 运动计划应根据个人体能调整，循序渐进
4. 营养补充剂不能替代饮食和运动
5. 腾讯文档需要网络连接

## 🔧 自定义修改

- **修改方案模板**：编辑 `templates/健康管理方案模板.md`
- **修改MDX模板**：编辑 `templates/健康跟踪表模板.mdx`
- **修改脚本**：编辑对应 `scripts/*.py` 文件
- **修改指标参考**：编辑 `references/指标参考范围.md`

## 📞 支持

如有问题，请检查：
1. Python版本 ≥ 3.8
2. 已安装 openpyxl（仅Excel功能需要）
3. 腾讯文档Token是否有效
4. 网络连接是否正常

---

*版本：1.1.0 | 更新日期：2026-03-31*
