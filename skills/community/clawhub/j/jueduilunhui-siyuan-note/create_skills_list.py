#!/usr/bin/env python3
"""
创建Skills列表文档到思源笔记
"""

import sys
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from siyuan_note_enhanced import create_enhanced_client
from datetime import datetime

def create_skills_list_document():
    """创建Skills列表文档"""
    print("=" * 70)
    print("创建Skills列表文档到思源笔记")
    print("=" * 70)

    # 创建客户端
    client = create_enhanced_client()

    # 文档内容
    content = f"""# Skills List - OpenClaw技能列表

## 📅 文档信息
- **创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **文档版本**: v1.0
- **技能总数**: 11个可用技能
- **状态**: 部分技能已配置并可用

---

## 📊 技能总览

### 状态统计
- ✅ **就绪 (Ready)**: 11个
- ❌ **缺失配置 (Missing)**: 44个

### 分类统计
- 📦 **Feishu生态**: 4个
- 🛠️ **开发工具**: 4个
- 🔧 **系统工具**: 3个

---

## ✅ 可用技能详情

### 📦 Feishu生态 (4个)

#### 1. 📝 feishu-doc
**描述**: Feishu document read/write operations. Activate when user mentions Feishu docs, cloud docs, or docx links.

**功能**:
- Feishu文档读写操作
- 支持cloud docs和docx链接
- 文档内容管理和编辑

**来源**: openclaw-extra

**状态**: ✅ Ready

**激活条件**: 当用户提到Feishu文档、云文档或docx链接时激活

---

#### 2. 💾 feishu-drive
**描述**: Feishu cloud storage file management. Activate when user mentions cloud space, folders, drive.

**功能**:
- Feishu云存储文件管理
- 文件夹和云端空间管理
- 文件上传、下载、移动等操作

**来源**: openclaw-extra

**状态**: ✅ Ready

**激活条件**: 当用户提到云空间、文件夹、drive时激活

---

#### 3. 🔐 feishu-perm
**描述**: Feishu permission management for documents and files. Activate when user mentions sharing, permissions, collaborators.

**功能**:
- Feishu权限管理
- 文档和文件的共享设置
- 协作者权限配置

**来源**: openclaw-extra

**状态**: ✅ Ready

**激活条件**: 当用户提到共享、权限、协作者时激活

---

#### 4. 📚 feishu-wiki
**描述**: Feishu knowledge base navigation. Activate when user mentions knowledge base, wiki, or wiki links.

**功能**:
- Feishu知识库导航
- Wiki链接处理
- 知识库内容检索

**来源**: openclaw-extra

**状态**: ✅ Ready

**激活条件**: 当用户提到知识库、wiki或wiki链接时激活

---

### 🛠️ 开发工具 (4个)

#### 5. 🧩 skill-creator
**描述**: Create or update AgentSkills. Use when designing, structuring, or packaging skills with scripts, references, and assets.

**功能**:
- 创建或更新AgentSkills
- 设计、结构化技能
- 打包技能和资源

**来源**: openclaw-bundled

**状态**: ✅ Ready

**激活条件**: 当设计、结构化或打包技能时激活

**使用场景**:
- 创建新的AI技能
- 更新现有技能
- 技能资源管理

---

#### 6. 🧵 tmux
**描述**: Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

**功能**:
- 远程控制tmux会话
- 交互式CLI操作
- 发送按键和抓取面板输出

**来源**: openclaw-bundled

**状态**: ✅ Ready

**激活条件**: 需要控制交互式CLI时激活

**使用场景**:
- 自动化终端操作
- 远程会话管理
- 批量任务执行

---

#### 7. 🌤️ weather
**描述**: Get current weather and forecasts (no API key required).

**功能**:
- 获取当前天气
- 天气预报查询
- 无需API密钥

**来源**: openclaw-bundled

**状态**: ✅ Ready

**激活条件**: 当用户查询天气时激活

**使用场景**:
- 日常天气查询
- 行程规划
- 活动安排

---

#### 8. 📝 siyuan-note ⭐
**描述**: 思源笔记读写技能，提供与思源笔记（SiYuan Note）进行交互的能力，包括读取和写入笔记内容

**版本**: v2.0 Enhanced

**功能**:
- ✅ 真正的独立文档创建（使用createDocWithMd API）
- ✅ 文章剪藏功能（类似Chrome扩展）
- ✅ 强大的模板渲染系统
- ✅ 笔记本和文档管理
- ✅ 内容搜索和查询
- ✅ 增强的错误处理

**来源**: openclaw-workspace

**状态**: ✅ Ready

**激活条件**: 当用户提到"查询思源笔记"、"写入思源笔记"、"创建思源笔记"等关键词时激活

**最新更新** (2026-02-17):
- 基于思源笔记Chrome扩展优化
- 实现真正的独立文档创建
- 新增文章剪藏和模板渲染功能
- 保持100%向后兼容

**使用示例**:
```python
from siyuan_note_enhanced import create_enhanced_client

# 创建独立文档
client = create_enhanced_client()
doc_id = client.create_document("其他", "文档名", "内容")

# 剪藏文章
client.clip_article("其他", "标题", "URL", "内容", tags=["技术"])

# 使用模板
result = client.render_template("${{title}}", {{'title': '测试'}})
```

---

### 🔧 系统工具 (3个)

#### 9. 🏥 healthcheck
**描述**: Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).

**功能**:
- 主机安全强化
- 风险容忍度配置
- 安全审计
- 防火墙/SSH/更新强化
- 风险态势评估
- 暴露审查
- 定期检查的OpenClaw cron调度
- 版本状态检查

**来源**: openclaw-bundled

**状态**: ✅ Ready

**激活条件**: 当用户要求安全审计、防火墙/SSH/更新强化、风险态势、暴露审查、定期安全检查或版本状态检查时激活

**适用系统**: 运行OpenClaw的机器（笔记本电脑、工作站、Pi、VPS）

---

#### 10. 📦 clawhub
**描述**: Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com. Use when you need to fetch new skills on the fly, sync installed skills to latest or a specific version, or publish new/updated skill folders with the npm-installed clawhub CLI.

**功能**:
- 搜索、安装、更新技能
- 从clawhub.com发布技能
- 同步技能到最新版本
- 技能版本管理

**来源**: openclaw-bundled

**状态**: ✅ Ready

**激活条件**: 需要获取新技能、同步已安装技能到最新版本或特定版本时激活

**使用方法**:
```bash
npx clawhub search skill-name
npx clawhub install skill-name
npx clawhub update skill-name
npx clawhub push skill-folder
```

---

#### 11. 📖 clawddocs
**描述**: Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features

**功能**:
- Clawdbot文档专家
- 决策树导航
- 搜索脚本
- 文档获取
- 版本跟踪
- 配置片段

**来源**: openclaw-workspace

**状态**: ✅ Ready

**激活条件**: 需要Clawdbot相关文档或配置时激活

---

## 📝 Skill状态说明

### 状态类型

#### ✅ Ready (就绪)
技能已配置完成，可以正常使用。

#### ❌ Missing (缺失)
技能需要额外的配置或依赖项未安装。

---

## 🗂️ Skills分类

### 按功能分类

| 分类 | 技能数量 | 技能列表 |
|------|---------|---------|
| Feishu生态 | 4 | feishu-doc, feishu-drive, feishu-perm, feishu-wiki |
| 开发工具 | 4 | skill-creator, tmux, weather, clawhub |
| 系统工具 | 3 | healthcheck, clawddocs, siyuan-note |

### 按来源分类

| 来源 | 数量 | 技能列表 |
|------|------|---------|
| openclaw-extra | 4 | Feishu系列 |
| openclaw-bundled | 5 | skill-creator, tmux, weather, healthcheck, clawhub |
| openclaw-workspace | 2 | clawddocs, siyuan-note |

---

## 💡 使用建议

### 优先使用

**1. siyuan-note** - 最常用
- 日常笔记管理
- 知识库建设
- 对话记录归档

**2. feishu-doc** - 文档协作
- 团队文档编写
- 多人协作编辑
- 云文档管理

**3. healthcheck** - 安全维护
- 定期安全检查
- 系统加固
- 风险评估

**4. weather** - 日常查询
- 天气预报获取
- 活动规划
- 出行参考

---

## 🔧 配置建议

### Feishu生态配置

要完整使用Feishu系列技能，需要：

1. **Feishu应用权限**:
   - 文档读写权限
   - 云存储访问权限
   - 知识库浏览权限
   - 权限管理权限

2. **API密钥配置**:
   - 在OpenClaw配置中添加Feishu App ID和App Secret

### siyuan-note配置

要使用思源笔记技能，需要：

1. **思源笔记设置**:
   - 启用API服务
   - 获取API token
   - 确保网络访问正常

2. **配置文件**:
   ```json
   {{
     "api_url": "http://localhost:6811",
     "token": "your-api-token",
     "default_notebook": "默认笔记本"
   }}
   ```

---

## 📚 相关资源

### 官方文档
- [OpenClaw文档](https://docs.openclaw.ai)
- [ClawHub](https://clawhub.com)
- [Feishu开放平台](https://open.feishu.cn/)
- [思源笔记官方](https://siyuan-note.com/)

### 技能开发
- [skill-creator](#5--skill-creator) - 创建自定义技能
- [clawhub](#10--clawhub) - 搜索和安装技能
- [SKILL.md规范](https://docs.openclaw.ai/agent-skills/)

---

## 🆕 最近更新

### 2026-02-17 v2.0
**siyuan-note技能重大升级**:
- ✅ 真正的独立文档创建
- ✅ 文章剪藏功能
- ✅ 强大的模板系统
- ✅ 基于思源笔记Chrome扩展优化

详细文档查看: [思源笔记技能v2.0升级总结](https://github.com/siyuan-note/siyuan-chrome)

---

## 🎯 快速开始

### 查询可用Skills
```bash
openclaw skills list
```

### 使用特定Skill
根据技能描述中的激活条件，直接在对话中提及相关关键词即可激活相应技能。

### 安装新Skills
```bash
npx clawhub search skill-name
npx clawhub install skill-name
```

---

## 📞 支持与反馈

如遇到问题，可以：
1. 查看[OpenClaw文档](https://docs.openclaw.ai)
2. 在[ClawHub](https://clawhub.com)搜索解决方案
3. 查看技能的SKILL.md文件获取详细说明

---

*本文档由OpenClaw自动生成* 🤖  
*更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*技能总数: 11/55*  
*版本: v1.0*
"""

    # 创建文档
    print("\n📝 创建Skills列表文档...")
    print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 统计: 11个可用技能/55个总技能")

    doc_id = client.create_document(
        "其他",
        "skills_list",
        content,
        tags=[" Skills", "文档", "OpenClaw"]
    )

    if doc_id:
        print(f"\n✅ 文档创建成功!")
        print(f"📄 文档ID: {doc_id}")
        print(f"📁 位置: 思源笔记 -> 其他 -> skills_list.sy")
        print(f"🏷️  标签: Skills, 文档, OpenClaw")
        
        # 验证文档
        print("\n🔍 验证文档创建...")
        docs = client.get_documents(client.get_notebook_id("其他"))
        
        found = False
        for doc in docs:
            if "skills_list" in doc.get('name', ''):
                found = True
                print(f"✅ 验证成功: 文档存在于列表中!")
                print(f"   📄 名称: {doc.get('name')}")
                print(f"   🆔 ID: {doc.get('id')}")
                break
        
        if found:
            print(f"\n🎉 完美! Skills列表文档已成功创建并可以在思源笔记中查看!")
            return True
        else:
            print(f"\n⚠️  文档可能正在同步，请稍后在思源笔记中查看")
            return False
    else:
        print("\n❌ 文档创建失败")
        return False

if __name__ == "__main__":
    success = create_skills_list_document()
    
    print("\n" + "=" * 70)
    if success:
        print("🎊 任务完成!")
        print("\n📝 Skills列表文档内容:")
        print("• 总览: 11个可用技能/55个总技能")
        print("• Feishu生态: 4个技能")
        print("• 开发工具: 4个技能")
        print("• 系统工具: 3个技能")
        print("• 包含详细的功能说明和使用示例")
        print("\n💡 现在可以在思源笔记中查看完整的Skills列表文档!")
    else:
        print("❌ 任务失败，请检查连接和配置")
    print("=" * 70)
