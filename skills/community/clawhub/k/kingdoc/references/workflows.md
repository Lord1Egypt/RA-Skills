# 常见工作流

> 本文档列举 KingDoc 的核心使用工作流。

---

## 工作流 1：文字文档创建 + 编辑

```python
# Step 1: 创建空文档
result = kdoc.file.create(name="会议纪要", type="doc")
file_id = result["data"]["file_id"]

# Step 2: 本地生成 DOCX 内容
from local.docx_gen import DocxGenerator
gen = DocxGenerator()
gen.add_heading("会议纪要", level=1)
gen.add_paragraph("会议时间：2026-07-02")
gen.add_paragraph("参会人员：张三、李四、王五")
gen.add_bullet_list(
    ["Q2 业绩回顾", "Q3 目标规划", "资源调配讨论"],
    title="议题"
)
gen.save("/tmp/meeting_notes.docx")

# Step 3: 上传覆盖
with open("/tmp/meeting_notes.docx", "rb") as f:
    content = f.read()
kdoc.file.upload_content(file_id=file_id, content=content)

return f"文档已创建: https://docs.wps.cn/doc/{file_id}"
```

---

## 工作流 2：批量导入 Excel

```python
# Step 1: 创建工作表
result = kdoc.et.create(name="客户数据导入")
sheet_id = result["data"]["sheet_id"]

# Step 2: 准备数据
data = []
data.append(["客户名", "联系电话", "地址", "签约金额"])
for customer in customer_list:
    data.append([
        customer.name,
        customer.phone,
        customer.address,
        customer.amount
    ])

# Step 3: 批量写入（必须用批量接口，禁止循环写入）
kdoc.et.range.write(
    sheet_id=sheet_id,
    range=f"A1:D{len(data)}",
    values=data
)

# Step 4: 设置公式（总计）
row_count = len(data)
kdoc.et.formula.set(
    sheet_id=sheet_id,
    cell=f"D{row_count+1}",
    formula=f"=SUM(D2:D{row_count})"
)

# Step 5: 添加图表
kdoc.et.chart.add(
    sheet_id=sheet_id,
    chart_type="bar",
    data_range=f"A1:D{row_count}",
    title="客户签约金额统计"
)

return f"导入完成，共 {len(customer_list)} 条记录"
```

---

## 工作流 3：多维表格完整 CRUD

```python
# Step 1: 创建表格
kdoc.dbt.create(name="项目管理")

# Step 2: 定义字段
kdoc.dbt.field.add(table_id, name="项目名称", type="text", required=True)
kdoc.dbt.field.add(table_id, name="负责人", type="text")
kdoc.dbt.field.add(table_id, name="优先级", type="select", options=["P0", "P1", "P2"])
kdoc.dbt.field.add(table_id, name="截止日期", type="date")
kdoc.dbt.field.add(table_id, name="进度", type="percent")
kdoc.dbt.field.add(table_id, name="备注", type="text")

# Step 3: 批量添加记录（必须用 add_batch，禁止循环 add）
records = [
    {"项目名称": "知识库建设", "负责人": "张三", "优先级": "P1"},
    {"项目名称": "API 网关升级", "负责人": "李四", "优先级": "P0"},
    {"项目名称": "前端重构", "负责人": "王五", "优先级": "P2"},
]
kdoc.dbt.record.add_batch(table_id, records=records)

# Step 4: 添加视图
kdoc.dbt.view.add(
    table_id=table_id,
    name="按优先级分组",
    type="group",
    config={"field": "优先级", "order": ["P0", "P1", "P2"]}
)

# Step 5: 设置 Webhook（事件监听）
kdoc.dbt.webhook.set(
    table_id=table_id,
    callback_url="https://your-app.com/webhook",
    events=["record.add", "record.update"]
)
```

---

## 工作流 4：回收站恢复

```python
# Step 1: 查询回收站
result = kdoc.trash.list(limit=50)
items = result["data"]["items"]

if not items:
    return "回收站是空的"

# Step 2: 展示给用户选择
return {
    "message": f"回收站有 {len(items)} 个项目",
    "items": items,
    "action": "用户选择要恢复的文件"
}

# Step 3: 用户确认后恢复
selected_file_id = user_selection
kdoc.trash.recover(file_id=selected_file_id)
return "已恢复"
```

---

## 工作流 5：版本回滚

```python
# Step 1: 查询版本历史
result = kdoc.version.list(file_id=file_id)
versions = result["data"]["versions"]

if len(versions) <= 1:
    return "只有一个版本，无法回滚"

# Step 2: 展示版本列表
for v in versions:
    print(f"v{v['version']}: {v['updated_at']} by {v['updater']}")

# Step 3: 用户选择目标版本
target_version = user_selection

# Step 4: 回滚
kdoc.version.restore(file_id=file_id, version=target_version)
return f"已回滚到 v{target_version}"
```

---

## 工作流 6：权限批量变更

```python
# Step 1: 获取目标用户列表
members = [
    {"email": "张三@company.com", "role": "editor"},
    {"email": "李四@company.com", "role": "editor"},
    {"email": "王五@company.com", "role": "viewer"},
]

# Step 2: 添加协作者（批量）
for member in members:
    kdoc.share.add_member(
        file_id=file_id,
        email=member["email"],
        role=member["role"]
    )

# Step 3: 可选：创建分享链接
result = kdoc.share.create_link(
    file_id=file_id,
    password="可选密码",
    expire_days=30,
    permission="edit"
)
return result["data"]["url"]
```

---

## 工作流 7：本地文件上传 + 分享

```python
import os

file_path = user_provided_path
if not os.path.exists(file_path):
    return "文件不存在"

# 检查文件大小（>100MB 走异步）
size_mb = os.path.getsize(file_path) / (1024 * 1024)

if size_mb > 100:
    # 异步上传
    result = kdoc.file.upload_large(file_path=file_path)
    task_id = result["data"]["task_id"]
    
    # 异步轮询进度
    while True:
        progress = kdoc.batch.query(task_id=task_id)
        if progress["status"] == "completed":
            file_id = progress["file_id"]
            break
        elif progress["status"] == "failed":
            return f"上传失败: {progress['error']}"
        time.sleep(2)
else:
    # 同步上传
    result = kdoc.file.upload(file_path=file_path)
    file_id = result["data"]["file_id"]

# 创建分享链接
share = kdoc.share.create_link(
    file_id=file_id,
    permission="edit",
    expire_days=7
)

return {
    "file_id": file_id,
    "share_url": share["data"]["url"],
    "message": f"上传成功，分享链接 7 天有效"
}
```

---

## 工作流 8：格式转换

```python
# Step 1: 提交转换任务
result = kdoc.office.convert(
    file_id=file_id,
    target_format="pdf"
)

# Step 2: 获取转换后的文件
converted_file_id = result["data"]["file_id"]

# Step 3: 下载
kdoc.file.download(file_id=converted_file_id, save_path="output.pdf")

return "转换完成"
```

---

## 工作流 9：纯文本提取

```python
# 从在线文档提取全文文字
result = kdoc.office.extract(file_id=file_id)
text = result["data"]["text"]

return f"提取到 {len(text)} 个字符"
```

---

## 工作流 10：通知推送

```python
# 企微机器人消息推送
kdoc.notification.send(
    channel="wecom",
    webhook_key="企微Webhook Key",
    content={
        "msgtype": "markdown",
        "markdown": {
            "content": "**文档已更新**\n> 文档：<https://docs.wps.cn/doc/abc|Q2 报告>\n> 更新人：张三\n> 时间：2026-07-02 14:00"
        }
    }
)

return "已推送通知"
```

---

## 工作流 11：批量任务状态轮询

```python
import time

# 提交批量复制任务
result = kdoc.batch.create(
    operation="copy",
    file_ids=["file_1", "file_2", "file_3"],
    target_folder_id="folder_xxx"
)
task_id = result["data"]["task_id"]

# 轮询进度
max_wait = 300  # 最多等 5 分钟
start = time.time()
while time.time() - start < max_wait:
    status = kdoc.batch.query(task_id=task_id)
    if status["data"]["status"] == "completed":
        return f"成功处理 {status['data']['success_count']} 个文件"
    elif status["data"]["status"] == "failed":
        return f"失败: {status['data']['error']}"
    time.sleep(3)

return "任务仍在后台运行，请稍后查看"
```

---

*最后更新：2026-07-02*
