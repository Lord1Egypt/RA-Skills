# K8sSkill - Kubernetes智能诊断助手

基于SRE最佳实践的Kubernetes智能诊断工具，支持在IDE内通过自然语言对话执行诊断。

## 快速开始

### 1. 安装依赖

```bash
cd <skill所在目录>
pip install -r requirements.txt
```

例如，如果skill放在某个目录下：
```bash
cd <skill所在目录>
pip install -r requirements.txt
```

### 2. 配置Kubernetes连接

**方式A: 使用项目自带的kubeconfig（已配置）**

项目已在 `config/` 目录下配置了kubeconfig文件：
- `config/k8s-Test-admin.conf`

**方式B: 手动配置到默认位置**
```bash
# 复制kubeconfig到默认位置（Linux/macOS）
cp ~/.kube/config.backup ~/.kube/config.backup 2>/dev/null || true
cp /path/to/your/kubeconfig ~/.kube/config
```

**方式C: 设置环境变量**
```powershell
# 设置KUBECONFIG环境变量指向skill目录下的配置文件（Windows）
$env:KUBECONFIG="<skill目录>\config\k8s-Test-admin.conf"
```

### 3. 在IDE中使用

**无需手动执行任何命令！** 直接在Trae IDE对话中描述你想检查的问题即可。

### 示例对话

**你:** "检查Pod为什么崩溃"

**AI:** 自动调用k8sskill诊断并返回结果

**支持的查询类型:**
- **Pod问题**: "检查Pod为什么崩溃" / "为什么有Pod一直在重启"
- **Deployment问题**: "部署失败了怎么回事" / "deployment rollout卡住了"
- **Service问题**: "为什么服务无法访问" / "访问不了我的服务"
- **节点问题**: "节点有问题" / "检查节点健康状态"
- **存储问题**: "存储绑定失败" / "PVC无法挂载"
- **事件日志**: "查看最近事件" / "集群有什么警告"
- **全量检查**: "集群有什么问题" / "检查所有资源"

### 4. Python API使用（高级）

开发者可以直接在Python中使用k8sskill：

```python
# 在 scripts/ 目录下执行
from orchestrator import AnalyzerOrchestrator, analyze_cluster

# 方式1: 使用编排器
orchestrator = AnalyzerOrchestrator()
results = orchestrator.analyze("检查集群问题")
print(orchestrator.format_report(results))

# 方式2: 使用便捷函数
report = analyze_cluster("检查Pod为什么崩溃", "production")
print(report)
```

---

## 故障排查

### 连接失败

```bash
# 检查kubeconfig是否存在
dir config\

# 手动测试连接
python -c "from kubernetes import config; config.load_kube_config('config/k8s-Test-admin.conf'); print('OK')"
```

### 权限不足

```bash
# 检查kubectl权限
kubectl auth can-i list pods

# 检查当前上下文
kubectl config current-context
```

### 模块导入错误

```python
# 确保在 scripts/ 目录下执行
# 错误方式: from scripts import AnalyzerOrchestrator
# 正确方式: from orchestrator import AnalyzerOrchestrator

# 验证导入是否正常
from orchestrator import AnalyzerOrchestrator
print("导入成功!")
```

---

## 特性

- **21个Kubernetes资源分析器** - 覆盖Pod、Deployment、Service、Node、PVC等核心资源
- 自然语言意图识别 - 直接对话即可诊断集群问题
- 中文和英文支持 - 全中文文档和错误提示
- 结构化诊断报告 - 清晰的故障分类和修复建议
- 模块化设计 - 按需加载，易于扩展
- 纯Python实现 - 基于kubernetes-python客户端
- 自动kubeconfig检测 - 支持环境变量、默认位置和项目配置

---

## 版本历史

- **v1.0.0** - 重大重构：模块化架构升级，提取BaseAnalyzer，新增orchestrator.py编排器（21个分析器）
- **v0.5.2** - 优化错误提示，新增verify_k8s_connection()连接验证函数（21个分析器）
- **v0.4.0** - 添加Secret、Gateway、HTTPRoute、Webhook分析器（21个分析器）
- **v0.3.0** - 添加ReplicaSet、NetworkPolicy、PDB、Storage、Security分析器（17个分析器）
- **v0.2.0** - 添加StatefulSet、Job、CronJob、HPA、ConfigMap、PVC、Node、Ingress、Event分析器（12个分析器）
- **v0.1.0** - 初始版本，Pod、Deployment、Service分析器（3个分析器）

---

## 许可证

基于Kubernetes最佳实践和SRE经验设计
