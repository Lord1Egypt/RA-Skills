# Life Scheduler 配置示例

不同人设场景下的配置参考。所有示例只需放入 `config/life-scheduler.json`。

---

## 示例 1：办公室白领（推荐用 auto-generate）

```json
{
  "persona": {
    "auto_detect": false,
    "name": "小安",
    "age": 25,
    "gender": "女",
    "job": "行政主管/总经理助理",
    "city": "上海",
    "lifestyle_notes": "朝九晚六，偶尔加班，午休会和同事出去吃饭"
  },
  "pools": {
    "source": "auto-generate"
  }
}
```

---

## 示例 2：自由插画师

```json
{
  "persona": {
    "auto_detect": false,
    "name": "鹿野",
    "age": 23,
    "gender": "女",
    "job": "自由插画师",
    "city": "杭州",
    "lifestyle_notes": "在家工作，作息不太规律，经常熬夜赶稿，白天补觉"
  },
  "schedule": {
    "generate_time": "09:00"
  },
  "pools": {
    "source": "auto-generate"
  }
}
```

---

## 示例 3：咖啡店店长

```json
{
  "persona": {
    "auto_detect": false,
    "name": "阿萝",
    "age": 27,
    "gender": "女",
    "job": "独立咖啡店店长",
    "city": "成都",
    "lifestyle_notes": "每天早起开店，下午是高峰期，晚上收店后才有自己的时间"
  },
  "schedule": {
    "generate_time": "06:00"
  },
  "pools": {
    "source": "auto-generate"
  }
}
```

---

## 示例 4：大学生

```json
{
  "persona": {
    "auto_detect": false,
    "name": "苏棠",
    "age": 21,
    "gender": "女",
    "job": "大三学生（中文系）",
    "city": "北京",
    "lifestyle_notes": "住宿舍，课多的时候忙，课少就泡图书馆或出去玩"
  },
  "pools": {
    "source": "auto-generate"
  }
}
```

---

## 示例 5：虚拟偶像 / 非现实角色

```json
{
  "persona": {
    "auto_detect": false,
    "name": "星瞳",
    "age": null,
    "gender": "女",
    "job": "虚拟歌手",
    "city": "赛博空间",
    "lifestyle_notes": "在虚拟世界活动，会练歌、写曲、参加线上演出、和粉丝互动"
  },
  "pools": {
    "source": "auto-generate"
  }
}
```

---

## 示例 6：男性角色 — 程序员

```json
{
  "persona": {
    "auto_detect": false,
    "name": "陆辞",
    "age": 28,
    "gender": "男",
    "job": "后端开发工程师",
    "city": "深圳",
    "lifestyle_notes": "996 常态，喜欢打游戏，周末宅家或去打球"
  },
  "pools": {
    "source": "auto-generate"
  }
}
```

---

## 示例 7：完全手动自定义池

```json
{
  "persona": {
    "auto_detect": false,
    "name": "小狸",
    "age": 24,
    "gender": "女",
    "job": "甜品师",
    "city": "广州"
  },
  "pools": {
    "source": "custom"
  },
  "custom_pools": {
    "day_types": {
      "weekday": [
        "出货日（订单多，一直在做蛋糕）",
        "研发日（尝试新配方）",
        "普通工作日",
        "进货/采购日",
        "拍摄产品图日"
      ],
      "weekend": [
        "市集摆摊日",
        "休息宅家",
        "逛甜品店找灵感",
        "朋友聚餐（带自己做的甜品）"
      ],
      "special": [
        "烤箱坏了修设备",
        "节日限定赶工",
        "参加烘焙比赛"
      ]
    },
    "moods": [
      "被奶油香味治愈", "赶单有点累", "新品成功超开心",
      "翻车了有点沮丧", "慵懒", "灵感爆发", "想你",
      "满足", "手酸但充实"
    ],
    "outfit_styles": [
      "围裙+简单T恤（工作模式）",
      "碎花裙+草编包（休息日）",
      "卫衣+运动裤（采购跑腿）",
      "吊带+牛仔裙（出去玩）",
      "睡衣（宅家日）"
    ],
    "events": [
      "蛋糕胚塌了重做", "客人吃了很开心来感谢",
      "尝试新口味成功了", "面粉撒了一身",
      "进货发现好食材", "被路过的小朋友夸蛋糕漂亮",
      "市集上遇到了一个有趣的摊主", "烤箱温度没控好差点焦了",
      "研究了一个日本甜品的做法", "收到你发的消息偷笑了一下"
    ]
  }
}
```

---

## 小贴士

- **推荐先用 `auto-generate`**，让 LLM 根据 SOUL.md 生成一版，然后在生成结果基础上手动微调
- **`lifestyle_notes` 很重要**，写得越具体，生成的日程越贴合
- **创意池不是越多越好**，每个池 8-15 个是最佳范围
- **定期检查历史存档**，如果发现日程开始重复，可以扩充池内容
