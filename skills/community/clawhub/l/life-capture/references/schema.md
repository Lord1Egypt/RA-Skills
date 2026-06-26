# Schema

The skill uses one index table plus type-specific child tables.

## entries
- `id`
- `type`
- `date`
- `time`
- `title`
- `raw_text`
- `summary`
- `source`
- `md_file`
- `md_anchor`
- `payload_json`
- `created_at`
- `updated_at`

## expenses
- `entry_id`
- `amount`
- `currency`
- `category`
- `subcategory`
- `pay_method`
- `merchant`

## tasks
- `entry_id`
- `status`
- `priority`
- `project`
- `due_date`
- `completed_at`

## schedules
- `entry_id`
- `schedule_date`
- `start_time`
- `end_time`
- `location`
- `status`

## ideas
- `entry_id`
- `idea_type`
- `status`
- `related_task_id`

## tags
- `id`
- `name`

## entry_tags
- `entry_id`
- `tag_id`
