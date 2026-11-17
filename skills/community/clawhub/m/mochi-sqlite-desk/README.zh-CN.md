# SQLite 数据查询与导出

[English](README.md)

查看 SQLite 表结构、运行只读查询、导出 CSV/JSON，并把 CSV 导入新的 SQLite 数据库。

## 功能

查看 SQLite 表结构、运行只读查询、导出 CSV/JSON，并把 CSV 导入新的 SQLite 数据库。

在当前助手的工作区运行，输出处理结果和报告，原文件保留。

## 用法示例

安装后，把任意一条发给 AI，并附上相关文件或网址。

```text
看看这个SQLite文件有哪些表和字段，先不要修改数据。
```

```text
按月份统计订单数量和金额，导出CSV，原数据库保持不变。
```

```text
把这份CSV导入一个新的SQLite文件，编号保留前导零，再检查完整性。
```

## 运行要求

Python 3.10+，标准库

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-sqlite-desk
```

也可在本页领取 ZIP，将其中的技能目录放入当前助手工作区的 `skills/` 文件夹。安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

## 补充示例与操作要点

- 看看这个SQLite文件有哪些表和字段，先不要修改数据。

- 按月份统计订单数量和金额，导出CSV，原数据库保持不变。

- 把这份CSV导入一个新的SQLite文件，编号保留前导零，再检查完整性。

Author / 作者：MochiLab · https://mochilab.bz
