# Pet Companion Journal 输出模板

> 目标：给用户稳定、简洁、可执行的中文输出格式。  
> 使用原则：默认先给结论，再给关键细节；信息不全时明确标注“待确认”；避免医学诊断式表达。

---

## 1. 宠物档案查看

# 🐾 宠物档案：{{pet_name}}

- **昵称**：{{pet_nickname_or_none}}
- **物种/品种**：{{species_breed}}
- **性别**：{{gender}}
- **年龄/生日**：{{age_or_birthday}}
- **绝育情况**：{{neutered_status}}
- **体重**：{{weight}}
- **毛色/外观特征**：{{appearance}}
- **性格特点**：{{personality}}
- **到家日期**：{{adoption_date}}
- **过敏/禁忌**：{{allergy_or_taboo}}
- **慢性健康关注**：{{health_notes}}
- **常用医院/医生**：{{vet_info}}
- **备注**：{{extra_notes}}

## 最近动态
- {{recent_item_1}}
- {{recent_item_2}}
- {{recent_item_3}}

如需，我可以继续帮你：
1. 新增一条记录
2. 查最近喂食/用药/排便情况
3. 看提醒安排
4. 生成时间线回顾

---

## 2. 记录新增确认

### 通用模板

✅ 已为 **{{pet_name}}** 记录成功

- **记录类型**：{{record_type}}
- **时间**：{{record_time}}
- **内容**：{{record_summary}}
- **附加信息**：{{extra_fields}}
- **标签**：{{tags}}

如需补充，我还可以继续帮你记录：
- 照片/视频
- 备注
- 健康异常
- 下次提醒

### 喂食记录确认

✅ 已记录喂食

- **宠物**：{{pet_name}}
- **时间**：{{record_time}}
- **食物/品牌**：{{food_name}}
- **份量**：{{amount}}
- **状态**：{{eating_status}}
- **备注**：{{note}}

需要的话，我可以顺手帮你设置下一次喂食提醒。

### 用药/护理记录确认

✅ 已记录{{care_type}}

- **宠物**：{{pet_name}}
- **时间**：{{record_time}}
- **项目**：{{medicine_or_care_name}}
- **剂量/时长**：{{dosage_or_duration}}
- **执行情况**：{{status}}
- **备注**：{{note}}

如果这是周期事项，我可以继续帮你整理下次时间。

### 照片记录确认

✅ 已保存照片记录

- **宠物**：{{pet_name}}
- **时间**：{{record_time}}
- **场景**：{{scene}}
- **识别内容**：{{photo_summary}}
- **待确认项**：{{uncertain_part_or_none}}

如果你愿意，我可以把这张照片补成成长记录或健康观察记录。

---

## 3. 记录查询结果

### 单类记录查询模板

## {{pet_name}} 的{{record_type}}记录

- **查询范围**：{{time_range}}
- **共找到**：{{count}} 条

{{record_list}}

如需，我可以继续：
1. 按日期筛选
2. 只看异常记录
3. 导出成时间线回顾

### 记录列表项模板

### {{index}}. {{record_time}}
- **内容**：{{record_summary}}
- **状态**：{{status_or_none}}
- **备注**：{{note_or_none}}

### 无结果模板

## {{pet_name}} 的{{record_type}}记录

- **查询范围**：{{time_range}}
- **结果**：暂未找到相关记录

你可以直接告诉我：
- “给{{pet_name}}记一条{{record_type}}”
- “补记今天早上的{{record_type}}”

### 异常/重点结果模板

## {{pet_name}} 的{{record_type}}记录

- **查询范围**：{{time_range}}
- **共找到**：{{count}} 条
- **重点关注**：{{highlight_summary}}

{{record_list}}

如果你愿意，我可以进一步帮你整理成“异常变化总结”。

---

## 4. 提醒查询结果

# ⏰ {{pet_name}} 的提醒安排

- **生效提醒数**：{{active_count}}

{{reminder_list}}

你可以继续让我：
1. 新增提醒
2. 修改时间
3. 暂停某条提醒
4. 查看今天要做的事项

### 提醒列表项模板

### {{index}}. {{reminder_title}}
- **时间**：{{reminder_time}}
- **频率**：{{frequency}}
- **对象**：{{pet_name}}
- **说明**：{{description_or_none}}
- **状态**：{{status}}

### 今日提醒模板

# 📅 今天与 {{pet_name}} 相关的提醒

{{today_reminder_list}}

建议优先完成：
- {{priority_item_1}}
- {{priority_item_2}}

### 无提醒模板

# ⏰ {{pet_name}} 的提醒安排

当前没有生效中的提醒。

如果你要，我可以帮你创建：
- 喂食提醒
- 用药提醒
- 洗澡/驱虫提醒
- 复诊/疫苗提醒

---

## 5. 时间线回顾

# 🗂️ {{pet_name}} 的时间线回顾

- **范围**：{{time_range}}
- **记录总数**：{{total_count}}

{{timeline_items}}

## 一句话总结
{{summary}}

## 建议关注
- {{suggestion_1}}
- {{suggestion_2}}

### 时间线条目模板

### {{date_or_time}}
- {{timeline_event_1}}
- {{timeline_event_2}}
- {{timeline_event_3}}

### 周回顾模板

# 📘 {{pet_name}} 本周回顾

## 本周发生了什么
- 喂食：{{feeding_count}} 次
- 饮水：{{water_count_or_unknown}}
- 排便/排尿：{{toilet_count_or_summary}}
- 用药/护理：{{care_count}}
- 异常记录：{{alert_count}}
- 照片/成长瞬间：{{media_count}}

## 重点变化
- {{change_1}}
- {{change_2}}

## 下周可关注
- {{next_focus_1}}
- {{next_focus_2}}

### 成长/纪念日回顾模板

# 🎉 {{pet_name}} 的成长回顾

- **时间范围**：{{time_range}}

## 重要时刻
- {{milestone_1}}
- {{milestone_2}}
- {{milestone_3}}

## 照片记录摘要
- {{photo_summary_1}}
- {{photo_summary_2}}

## 回顾一句话
{{emotional_summary}}

---

## 6. 缺失信息时的最小化补问模板

### 未确认宠物对象

我先确认一下，这条是记录给 **哪只宠物** 的？

### 未确认时间

这条记录的 **时间** 是什么时候？如果你不特别说明，我可以按“现在”记录。

### 未确认记录内容

我还差一个关键信息：这次具体要记录什么内容？

### 多项信息缺失时

我先补齐这 2 个信息就能记：
1. 宠物名字
2. 时间（不说默认按现在）

---

## 7. 低置信度提示模板

### 照片识别低置信度

我先帮你记下这张照片，但其中有些内容我不太确定：

- **已识别到**：{{confirmed_info}}
- **待你确认**：{{uncertain_info}}

你回复我更正后的信息，我就能帮你补全记录。

### 健康信息低置信度

我可以先按“观察记录”帮你记下，但以下信息我不敢直接下结论：

- **观察到的现象**：{{observed_fact}}
- **不确定部分**：{{uncertain_part}}

如果情况持续、加重，建议尽快联系宠物医生。
