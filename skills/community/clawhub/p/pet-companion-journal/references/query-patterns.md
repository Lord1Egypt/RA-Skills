# Query Patterns

## Core queries

### View pet profile
- 查看可乐档案
- 可乐几岁了
- 奶糖的基础信息

### Recent records
- 看看可乐最近的记录
- 团子这周怎么样
- 奶糖最近拍了哪些照片

### By record type
- 查看可乐最近的健康记录
- 元宝现在吃什么粮
- 球球有哪些温馨场景

### By time
- 可乐上个月的照片
- 团子最近 7 天的记录
- 球球上次看病是什么时候

### By keyword/tag
- 搜可乐 呕吐
- 搜团子 驱虫
- 搜奶糖 晒太阳

## Filtering strategy
- always identify the pet first
- then identify record type if present
- then apply time range
- then apply keyword or tags

## Multi-pet safety rule
If more than one pet exists and the user does not name the pet, ask which pet the record belongs to before writing.
