# API Contract And Errors

Task lifecycle:

1. `GET /open/v1/product/list`
2. `POST /open/v1/tasks/create`
3. `POST /open/v1/tasks/detail`

Create fails immediately on non-zero API codes or missing task ID.

Polling succeeds only when the first completed media exposes a usable URL and no media entry has entered a failed or deleted state.

Timeout contract:

- request timeout for product list, task create, and task detail: 30 seconds per call
- upload timeout: 60 seconds
- poll interval: 5 seconds
- total generation timeout: 600 seconds
