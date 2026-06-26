# MooTeam API Usage Guide (Unified Client)

## 1. Конфигурация
Все запросы проходят через класс `MooTeamClient`. 
**Важно:** Перед выполнением действий модель должна убедиться, что загружены переменные:
- `MOOTEAM_API_TOKEN`
- `MOOTEAM_COMPANY_ALIAS`

## 2. Справочник методов (Endpoints)

### Проекты (Projects)
- `get_projects()`: Получение всех проектов.
- `create_project(title, description)`: Создание нового проекта.
- `get_project_details(id)`: Инфо по конкретному проекту.
- `delete_project(id)`: Удаление проекта.

### Задачи (Tasks)
- `get_tasks(project_id, status_id)`: Список задач. Фильтры опциональны.
- `create_task(title, project_id, **kwargs)`: Создание задачи. 
  *Доп. поля в kwargs:* `description`, `status_id`, `assigned_to`, `priority`.
- `update_task(task_id, data)`: Изменение любых свойств задачи.
- `delete_task(task_id)`: Удаление.

### Рабочие процессы и Статусы (Workflows & Statuses)
*Используй эти методы, чтобы узнать, какие ID статусов передавать в задачи.*
- `get_task_workflows()`: Список процессов.
- `get_task_statuses()`: Список всех статусов (например: "Backlog", "In Progress").

### Метки (Labels)
- `get_task_labels()`: Список тегов.
- `get_task_label_groups()`: Группировка тегов.

### Таймер и Учет времени (Timer)
- `start_timer(task_id)`: Запуск трекинга для задачи.
- `stop_timer()`: Остановка текущего таймера.
- `get_timer_status()`: Проверка активного таймера.
- `get_task_time_list(task_id)`: История логов времени по задаче.
- `create_time_log(data)`: Ручная запись времени (через `/timer/create`).

### Логи активности (Activity Logs)
- `get_activity_logs()`: Лента всех событий в компании.

## 3. Инструкции для ИИ (System Instructions)

1. **Цепочки действий:** Если пользователь просит "Переведи задачу X в статус Готово", сначала вызови `get_task_statuses()`, найди ID статуса "Готово", а затем вызови `update_task()`.
2. **Конфликты таймера:** Перед вызовом `start_timer()` всегда проверяй `get_timer_status()`. Если таймер уже запущен на другой задаче, сначала вызови `stop_timer()`.
3. **Безопасность данных:** При выводе логов активности или списков задач, сокращай ответ для пользователя, оставляя только важные поля (ID, Название, Автор).