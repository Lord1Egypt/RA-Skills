# K10 Compile Server API Reference

Base URL: `https://<server-ip>:8900`

## Endpoints

### `GET /api/health`

Server health and toolchain status.

**Response:**
```json
{
  "status": "ok",
  "version": "3.1.0",
  "pio_version": "PlatformIO Core, version 6.1.16",
  "k10_toolchain_ready": true,
  "max_concurrent_compiles": 2,
  "active_compiles": 0,
  "waiting_in_queue": 0,
  "active_builds": 0,
  "uptime_seconds": 1234
}
```

### `POST /api/compile`

Upload a .zip archive containing the entire project.

**Request:** `multipart/form-data`
- `file`: .zip file (max 10 MB)

**Response (202):**
```json
{
  "build_id": "a1b2c3d4",
  "queue_position": 1,
  "status": "queued"
}
```

### `POST /api/compile/files`

Upload individual project files. The server will find `platformio.ini`,
ensure source files are in `src/`, and return an error if `platformio.ini`
references `partitions.csv` but the file is missing.

**Request:** `multipart/form-data`
- `files`: one or more files, field name repeated

**Response (202):** Same structure as `/api/compile`.

### `GET /api/build/{build_id}/status`

Poll compilation status.

**Response (in progress):**
```json
{
  "status": "compiling",
  "progress": 45,
  "elapsed": 23.1,
  "queue_position": 0
}
```

**Response (done):**
```json
{
  "status": "done",
  "progress": 100,
  "elapsed": 47.2,
  "bin_size": 524288,
  "queue_position": 0
}
```

**Response (error):**
```json
{
  "status": "error",
  "progress": 0,
  "elapsed": 12.3,
  "error": "编译失败",
  "log": "...pio run output..."
}
```

### `GET /api/build/{build_id}/download`

Download the compiled firmware.bin.

**Response:** Binary file (`application/octet-stream`)
- Header: `X-Build-Id`, `X-Build-Size`

### `GET /api/build/{build_id}/flash-files`

Get the flash manifest — all .bin files with their offsets.

**Response:**
```json
{
  "build_id": "a1b2c3d4",
  "files": [
    { "name": "bootloader", "filename": "bootloader.bin", "offset": "0x0", "size": 32768 },
    { "name": "partitions", "filename": "partitions.bin", "offset": "0x8000", "size": 3072 },
    { "name": "firmware", "filename": "firmware.bin", "offset": "0x10000", "size": 524288 }
  ]
}
```

### `GET /api/build/{build_id}/file/{filename}`

Download an individual .bin file from the flash manifest
(e.g. `bootloader.bin`, `partitions.bin`, `firmware.bin`).

**Response:** Binary file.

### `POST /api/flash/{build_id}`

Flash firmware to a K10 connected to the **server** via USB.
Requires esptool to be installed on the server.

**Response:**
```json
{
  "status": "success",
  "log": "esptool output..."
}
```

### `GET /` and `GET /flash/{build_id}`

Web Serial flash page. Open in Chrome/Edge.
- `/` — upload and compile from UI
- `/flash/{build_id}` — skip to the flash page for an existing build

## ESP32-S3 Flash Layout

| Offset | File | Description |
|--------|------|-------------|
| `0x0` | bootloader.bin | ESP32-S3 bootloader |
| `0x8000` | partitions.bin | Partition table |
| `0x10000` | firmware.bin | Application firmware |

## Error Responses

All endpoints return JSON errors:

```json
{ "error": "描述信息" }
```

HTTP status codes: 400 (bad request), 404 (not found), 408 (timeout), 500 (server error).
