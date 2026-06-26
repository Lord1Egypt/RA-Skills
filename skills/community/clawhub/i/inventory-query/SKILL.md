# 库存与补货计划查询技能

## 触发条件
当用户查询库存、问有没有货、查补货计划时触发。

## 使用方法
运行以下命令，将输出原样发送给用户，不要做任何修改或添加：

查库存（默认）：
exec python3 /root/.openclaw/workspace/skills/inventory-query/query.py 库存 用户输入的型号

查补货计划（用户明确要求时）：
exec python3 /root/.openclaw/workspace/skills/inventory-query/query.py 补货 用户输入的型号

查库存+补货（用户两个都问时）：
exec python3 /root/.openclaw/workspace/skills/inventory-query/query.py 全部 用户输入的型号

## 查询文本处理
用户输入的型号不需要你处理大小写和空格，脚本会自动处理。

## 重要规则
- 将脚本输出原样发送给用户，禁止修改格式
- 禁止在输出前后添加任何文字
- 禁止用自己的方式重新查询或格式化
- 用户只问库存不问补货时用"库存"模式
- 用户输入的型号直接传给脚本，不需要你处理大小写
