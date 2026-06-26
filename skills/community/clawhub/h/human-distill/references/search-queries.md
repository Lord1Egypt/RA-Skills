# 全网搜索查询模板

占位符：`{name}` 人物名/昵称，`{topic}` 主题领域，`{course}` 课程或品牌名，`{handle}` 抖音号。

按用户主题从对应分区选 **6–10 条** 执行 `web_search`，勿一次堆砌超过 10 条。

## 通用（每人都跑）

```
"{name} {topic} 是谁 背景"
"抖音 {handle} 主页"
"{name} {topic} 访谈 OR 播客 OR 演讲"
"{name} {course}"
"{name} {topic} site:mp.weixin.qq.com OR site:zhihu.com"
```

## 营养 / 健身

```
"{name} {topic} 蛋白质 摄入"
"{name} {topic} 碳水 减脂"
"{name} {topic} 脂肪 饮食"
"{name} {topic} 补剂 肌酸 咖啡因"
"{name} {topic} 睡眠 恢复"
"{name} {topic} 备赛 增肌"
"{name} {topic} 训练前后 营养"
"{name} 营养矩阵 OR 运动营养 课程"
"{name} {topic} site:youtube.com"
```

## 投资 / 商业

```
"{name} {topic} 投资 方法论"
"{name} {topic} 案例 分析"
"{name} {topic} 争议 批评"
"{name} {course} 课程 评价"
"{name} 创业 访谈"
```

## 科技 / 产品

```
"{name} {topic} 观点"
"{name} {topic} 预测"
"{name} 播客 OR 演讲 {topic}"
```

## 平台定向（有线索时追加）

```
"{name} site:xiaohongshu.com {topic}"
"{name} site:bilibili.com {topic}"
"{name} site:weibo.com {topic}"
"{name} Instagram OR 学员 反馈 {course}"
```

## 排除噪声（用于理解人设，非主题蒸馏）

仅在需要完整画像时搜索，不写入主题蒸馏正文：

```
"{name} 带货 广告"
"{name} 直播 回放"
```
