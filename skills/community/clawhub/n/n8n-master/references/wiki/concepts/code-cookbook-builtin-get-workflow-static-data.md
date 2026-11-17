# `getWorkflowStaticData(type)`

## 何时读取

当用户的问题涉及 n8n 文档 `code/cookbook/builtin/get-workflow-static-data.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- This gives access to the static workflow data. As an example: you can save a timestamp of the last item processed from an RSS feed or database. It will always return an object. Properties can then read, delete or set on that object. When the workflow execution succeeds, n8n checks automatically if the data has changed and saves it, if necessary.

## 快速定位

- Templates and examples

