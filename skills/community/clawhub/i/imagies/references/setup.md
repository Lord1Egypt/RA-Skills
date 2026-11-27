# Connect to Imagies

Run Imagies using the [Docker deployment guide](https://psyb0t.github.io/docker-imagies/deployment/). Set `IMAGIES_URL` to its base URL, such as `http://localhost:8000`, and provide `IMAGIES_AUTH_TOKEN` when the server uses bearer authentication. The MCP endpoint is `/v1/mcp`. Include the request host in the server's `IMAGIES_MCP_ALLOWED_HOSTS` when connecting by proxy or container hostname.

For a local instance with no token, use these examples. Replace `IMAGE_ID` with an ID returned by staging or an operation. When authentication is enabled, send the configured bearer token in the `Authorization` header.

```sh
curl --fail-with-body \
  -H 'Content-Type: image/png' \
  --data-binary @input.png \
  "${IMAGIES_URL%/}/v1/images"

curl --fail-with-body \
  --output result.png \
  "${IMAGIES_URL%/}/v1/images/IMAGE_ID"
```

See the [REST reference](https://psyb0t.github.io/docker-imagies/api/) and [MCP guide](https://psyb0t.github.io/docker-imagies/mcp/).
