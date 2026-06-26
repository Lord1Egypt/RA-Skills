# 例子：分享知识库给同事

> 用户想把知识库分享给同事查看，生成一个只读分享链接。

## 用户输入

```
把「AI 论文集」分享给同事
```

## 调用链路

```
步骤 1 — 找到目标知识库
GET /api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50
→ 找到「AI 论文集」collectionId: "xxx"

步骤 2 — 创建分享链接
POST /api/v1/knowledge/shareNotebook
Body(JSON): {"collectionId": "xxx"}
→ data: "XaPR2vI%2BJl5%2BAES7NQSNz..."（加密分享 ID）

步骤 3 — 拼接分享链接
分享链接 = https://iflow.cn/inotebook/share?shareId={data}
→ https://iflow.cn/inotebook/share?shareId=XaPR2vI%2BJl5%2BAES7NQSNz...
```

## 展示给用户

```
知识库「AI 论文集」的分享链接已生成：
https://iflow.cn/inotebook/share?shareId=XaPR2vI%2BJl5%2BAES7NQSNz...

被分享者可查看知识库中的所有文件和已生成的内容（只读，不可编辑或再生成）。
```

## 关键规则

- 分享是**只读快照**，被分享者不能编辑、不能基于知识库生成新内容
- 分享链接格式固定为 `https://iflow.cn/inotebook/share?shareId={data}`
- `data` 是后端返回的加密字符串，直接拼接即可（可能包含 URL 编码字符如 `%2B`）
- 如果用户没指定哪个知识库，需要先查询列表让用户选择
