# Entry And Routing

The active CLI entrypoint is `scripts/ima_runtime_cli.py`.

Runtime flow:

1. parse CLI flags
2. normalize input images
3. build a `GatewayRequest`
4. resolve it into an image `TaskSpec`
5. fetch the live product list for `spec.task_type`
6. bind the model and execute the task

`build_image_task_spec()` is the authority for image routing:

- explicit `task_type` wins
- zero input images routes to `text_to_image`
- one or more input images routes to `image_to_image`
- reference or continuity intent without an image returns a `ClarificationRequest`
