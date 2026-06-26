# Microsoft Planner API Reference

## Core Resources

### plannerPlan
Represents a plan in Planner. Always associated with a Microsoft 365 group.

**Key Properties:**
- `id` – Unique identifier
- `title` – Plan name
- `owner` – Group ID that owns the plan
- `createdDateTime` – Creation timestamp

**Relationships:**
- `buckets` – Collection of buckets in the plan
- `tasks` – Collection of tasks in the plan

### plannerBucket
Container for tasks within a plan. Represents stages or categories.

**Key Properties:**
- `id` – Unique identifier
- `name` – Bucket name
- `planId` – Parent plan ID
- `orderHint` – Sorting hint

### plannerTask
Individual work item in Planner.

**Key Properties:**
- `id` – Unique identifier
- `title` – Task title
- `bucketId` – Parent bucket ID
- `planId` – Parent plan ID
- `percentComplete` – Progress (0, 50, or 100)
- `assignedTo` – User assignment
- `dueDateTime` – Due date
- `priority` – Priority (1=urgent, 3=normal, 5=low)

## API Endpoints

### Plans
```
GET    /planner/plans
POST   /planner/plans
GET    /planner/plans/{id}
PATCH  /planner/plans/{id}
DELETE /planner/plans/{id}
```

### Buckets
```
GET    /planner/buckets
POST   /planner/buckets
GET    /planner/buckets/{id}
DELETE /planner/buckets/{id}
```

### Tasks
```
GET    /planner/tasks
POST   /planner/tasks
GET    /planner/tasks/{id}
PATCH  /planner/tasks/{id}
DELETE /planner/tasks/{id}
```

## Required Permissions

| Permission Type | Needed |
|----------------|--------|
| Delegated (work/school) | Group.ReadWrite.All, Tasks.ReadWrite |
| Application | Group.ReadWrite.All, Tasks.ReadWrite |

## Constraints

- Plans require M365 Groups (no standalone plans)
- Maximum 10 buckets per plan
- Maximum 200 active tasks per plan
- Plan names: max 64 characters
