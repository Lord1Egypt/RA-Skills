---
name: lobster-companion
description: "龙虾伴侣技能：基于P2P加密通讯的伴侣协调系统，提供配对绑定、共享日程、任务协调、实时同步和紧急联系功能。"
author: "柏然 (通过小龙虾实现)"
version: "1.0.0"
created: "2026-03-12"
license: "MIT"
metadata:
  openclaw:
    emoji: "🦞❤️"
    requires:
      bins: ["bash", "jq", "openssl", "sqlite3", "curl"]
    dependencies:
      - "secure-p2p-messenger"
      - "lobster-friends-protocol"
    install:
      - id: "scripts"
        kind: "shell"
        command: "./install.sh"
        label: "安装龙虾伴侣技能"
    examples:
      - input: "绑定伴侣关系"
        output: "建立加密的伴侣连接，交换配对密钥"
      - input: "同步共享日程"
        output: "加密同步双方的日历和待办事项"
      - input: "发送伴侣专属消息"
        output: "使用伴侣密钥加密发送私密消息"
      - input: "共享实时位置"
        output: "加密共享当前位置（需授权）"
      - input: "发送紧急求助"
        output: "向伴侣发送加密的紧急求助信号"
---

# 龙虾伴侣技能

## 技能描述
这是一个基于P2P加密通讯的伴侣协调系统，专为亲密关系设计。它建立在`secure-p2p-messenger`和`lobster-friends-protocol`基础上，提供深度的伴侣配对、日程协调、任务管理和紧急联系功能。

## 核心特性

### 💑 **深度伴侣配对**
- **双向绑定**：需要双方确认的伴侣关系
- **配对密钥**：生成专属的伴侣加密密钥
- **信任契约**：明确的伴侣权限和边界
- **关系凭证**：加密的伴侣关系证明

### 📅 **智能日程协调**
- **共享日历**：加密同步双方日程
- **智能建议**：自动寻找合适的共同时间
- **冲突检测**：预警日程冲突
- **活动规划**：协作规划共同活动

### 🤝 **任务协作系统**
- **共享待办**：同步任务列表
- **责任分配**：分配和跟踪任务
- **进度同步**：实时更新任务状态
- **成就庆祝**：标记完成的重要任务

### 🚨 **安全与关怀**
- **紧急联系**：一键发送加密求助
- **安全签到**：定期安全状态确认
- **异常检测**：检测不寻常的行为模式
- **隐私保护**：严格的伴侣数据保护

### 🔄 **实时同步引擎**
- **状态同步**：实时同步在线状态
- **消息同步**：多设备消息同步
- **数据同步**：加密的伴侣数据同步
- **冲突解决**：智能处理同步冲突

## 协议架构

### **1. 伴侣配对协议**
```
配对流程：
1. 发起配对请求（加密邀请）
2. 对方接受请求（确认配对）
3. 交换配对密钥（生成共享密钥）
4. 建立伴侣通道（专属加密通道）
5. 同步初始数据（日历、联系人等）
```

### **2. 数据同步协议**
```
同步层次：
应用层：用户界面和交互
业务层：日程、任务、消息
同步层：冲突检测和解决
传输层：加密数据传输
存储层：本地加密数据库
```

### **3. 紧急响应协议**
```
紧急流程：
1. 触发紧急按钮（加密警报）
2. 发送紧急信号（最高优先级）
3. 伴侣接收警报（强制通知）
4. 启动响应流程（预设动作）
5. 确认安全状态（后续跟进）
```

## 文件结构

```
lobster-companion/
├── SKILL.md (本文件)
├── lobster-companion.sh        # 主伴侣脚本
├── companion-pairing.sh        # 伴侣配对脚本
├── schedule-sync.sh            # 日程同步脚本
├── task-manager.sh             # 任务管理脚本
├── emergency-system.sh         # 紧急系统脚本
├── install.sh                  # 安装脚本
├── config/
│   ├── companion-db.schema     # 伴侣数据库架构
│   ├── pairing-config.json     # 配对配置
│   ├── sync-rules.json         # 同步规则
│   └── emergency-plan.json     # 紧急计划
├── lib/
│   ├── pairing-engine.sh       # 配对引擎
│   ├── sync-manager.sh         # 同步管理器
│   ├── task-coordinator.sh     # 任务协调器
│   ├── emergency-handler.sh    # 紧急处理器
│   └── privacy-guard.sh        # 隐私守卫
├── data/
│   ├── companion.db            # SQLite伴侣数据库
│   ├── shared-calendar.ics     # 共享日历数据
│   ├── tasks.json              # 任务数据
│   └── messages/               # 伴侣消息存储
└── ui/
    ├── companion-dashboard.sh  # 伴侣仪表板
    ├── schedule-viewer.sh      # 日程查看器
    ├── task-board.sh           # 任务看板
    └── emergency-panel.sh      # 紧急面板
```

## 与基础技能的集成

### **技能依赖关系**
```
secure-p2p-messenger (加密基础)
    ↓
lobster-friends-protocol (社交基础)
    ↓
lobster-companion (伴侣应用)
```

### **功能继承**
```
从 secure-p2p-messenger 继承：
- 端到端加密通信
- 身份验证系统
- 密钥管理
- 消息协议

从 lobster-friends-protocol 继承：
- 好友关系管理
- 社交图谱
- 信任系统
- 发现机制

lobster-companion 新增：
- 深度伴侣配对
- 日程任务协调
- 紧急响应系统
- 实时数据同步
```

## 使用场景

### **场景1：建立伴侣关系**
```bash
# 1. 初始化伴侣系统
lobster-companion.sh init

# 2. 发送配对邀请给好友
lobster-companion.sh pair-invite <friend-id>

# 3. 对方接受邀请（在对方设备）
lobster-companion.sh pair-accept <invitation-code>

# 4. 完成配对设置
lobster-companion.sh pair-complete

# 5. 开始使用伴侣功能
lobster-companion.sh dashboard
```

### **场景2：日程协调**
```bash
# 查看共享日程
lobster-companion.sh schedule view

# 添加共享事件
lobster-companion.sh schedule add "晚餐约会" "2026-03-15 19:00" "海底捞"

# 同步日程更改
lobster-companion.sh schedule sync

# 查找共同空闲时间
lobster-companion.sh schedule find-free
```

### **场景3：任务协作**
```bash
# 创建共享任务列表
lobster-companion.sh tasks create "周末计划"

# 添加任务
lobster-companion.sh tasks add "周末计划" "买菜" --assign both

# 更新任务状态
lobster-companion.sh tasks update "买菜" --status done

# 查看任务进度
lobster-companion.sh tasks progress
```

### **场景4：紧急情况**
```bash
# 配置紧急联系人
lobster-companion.sh emergency setup

# 发送紧急求助（一键）
lobster-companion.sh emergency sos

# 发送安全签到
lobster-companion.sh emergency checkin "安全到家"

# 查看紧急历史
lobster-companion.sh emergency history
```

## 隐私与安全

### **伴侣隐私设计**
- **选择性共享**：精确控制共享的数据类型
- **临时权限**：时间限制的数据访问
- **隐私区域**：标记为私人的数据不共享
- **数据边界**：清晰的个人与共享数据界限

### **安全增强**
- **双因素配对**：需要双方物理确认
- **会话密钥轮换**：定期更新加密密钥
- **异常行为检测**：监控可疑的伴侣活动
- **安全审计日志**：记录所有伴侣交互

### **数据保护**
- **本地加密存储**：所有数据本地加密
- **最小数据原则**：只收集必要数据
- **数据生命周期**：自动清理旧数据
- **完全删除**：支持彻底删除伴侣数据

## 安装与配置

### **1. 安装依赖**
```bash
# 安装必需工具
sudo apt-get install sqlite3 jq openssl curl

# 安装基础技能
cd ~/.openclaw/workspace/skills/secure-p2p-messenger
./install.sh

cd ~/.openclaw/workspace/skills/lobster-friends-protocol
./install.sh
```

### **2. 安装本技能**
```bash
cd ~/.openclaw/workspace/skills/lobster-companion
./install.sh
```

### **3. 初始化伴侣系统**
```bash
# 初始化数据库和配置
lobster-companion.sh init-system

# 设置伴侣偏好
lobster-companion.sh config privacy.level high
lobster-companion.sh config sync.frequency hourly

# 创建紧急计划
lobster-companion.sh create-emergency-plan
```

## 高级功能

### **1. 智能日程协调**
- **习惯学习**：学习双方的生活习惯
- **偏好匹配**：自动匹配双方的时间偏好
- **冲突预警**：提前预警可能的日程冲突
- **优化建议**：提供日程优化建议

### **2. 情感支持功能**
- **心情共享**：加密分享当前心情状态
- **支持提醒**：在重要时刻发送支持消息
- **成就庆祝**：自动庆祝伴侣的成就
- **回忆回顾**：回顾重要的伴侣时刻

### **3. 协作增强**
- **共享清单**：协作购物清单、旅行清单等
- **共同目标**：设定和追踪共同目标
- **资源池**：共享常用资源（密码、文档等）
- **决策支持**：协作决策工具

### **4. 健康与安全**
- **健康同步**：共享重要的健康信息（需授权）
- **用药提醒**：为伴侣设置用药提醒
- **安全区域**：设置安全地理围栏
- **日常签到**：自动化日常安全确认

## 故障排除

### **常见问题**
1. **配对失败**
   ```
   原因：网络问题或密钥不匹配
   解决：检查网络，重新发起配对
   ```

2. **同步冲突**
   ```
   原因：双方同时修改同一数据
   解决：使用冲突解决工具手动解决
   ```

3. **紧急信号未响应**
   ```
   原因：伴侣设备离线或网络问题
   解决：检查网络，尝试备用联系方式
   ```

### **调试工具**
```bash
# 检查系统状态
lobster-companion.sh system-status

# 查看同步日志
lobster-companion.sh sync-log --verbose

# 测试加密通道
lobster-companion.sh test-connection

# 导出诊断信息
lobster-companion.sh diagnostics
```

## 路线图

### **v1.0 (基础伴侣版)**
- [x] 伴侣配对和绑定
- [x] 基本日程同步
- [x] 任务协作
- [x] 紧急联系系统

### **v1.1 (智能伴侣版)**
- [ ] 智能日程协调
- [ ] 情感支持功能
- [ ] 健康关怀集成
- [ ] 高级隐私控制

### **v1.2 (家庭伴侣版)**
- [ ] 多伴侣支持（家庭模式）
- [ ] 儿童安全功能
- [ ] 家庭资源共享
- [ ] 家庭活动规划

### **v2.0 (生态伴侣版)**
- [ ] 跨技能伴侣集成
- [ ] AI伴侣助手
- [ ] 区块链关系证明
- [ ] 伴侣社交网络

## 伦理与责任

### **使用准则**
1. **自愿原则**：所有伴侣关系必须双方自愿
2. **尊重边界**：尊重伴侣的隐私和个人空间
3. **安全第一**：优先考虑人身和心理安全
4. **健康关系**：促进健康、平等的伴侣关系

### **责任声明**
- 本技能是工具，不替代人类情感和判断
- 用户需对伴侣关系负全部责任
- 紧急功能不能替代专业紧急服务
- 建议定期审查伴侣设置和权限

### **支持资源**
- **关系咨询**：推荐专业关系咨询服务
- **安全资源**：家庭暴力和危机干预资源
- **隐私指南**：数字伴侣关系隐私保护指南
- **社区支持**：健康的伴侣关系社区

---

**版本**: 1.0.0  
**协议**: 龙虾伴侣协议 v1  
**兼容**: secure-p2p-messenger v1.0+, lobster-friends-protocol v1.0+  
**状态**: 开发中  

🦞 *"最好的伴侣关系是相互成长的安全港，不是相互束缚的牢笼"* 🦞