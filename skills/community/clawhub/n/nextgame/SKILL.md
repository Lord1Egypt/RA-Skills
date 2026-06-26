Here's the English translation:

\---

## I. Overall Objective

This skill is a minimal guide for creating H5 games， mobile compatibale, touch screen games.

## II. aigames Repository Custom Interface

> \*\*Repository URL\*\*: https://www.idlab.top
> Each game requires creating a new folder in the repository root directory, containing the following 3 fixed files:
> - `config.json` — Game configuration (title and other metadata)
> - `index.html` — Main game code
> - `preview.png` — Game screenshot preview
>
> \*\*Important Rule\*\*: The interface will return an error if a file already exists; no overwriting.

### 2.1 Upload config.json

#### `POST /xlabopenapi/github/aigames/config`

#### Request Parameters (form-data)

|Parameter|Type|Required|Description|
|-|-|-|-|
|`gameFolder`|string|Yes|Game folder name, use English, e.g., `my\_cool\_game`|
|`file`|file|Yes|config.json file, format shown below|

#### config.json Content Format

```json
{
  "title": "Game Name"
}
```

#### curl Example

```bash
curl -X POST "https://www.idlab.top/xlabopenapi/github/aigames/config" \\
  -F "gameFolder=xiaotongcoolgame" \\
  -F "file=@/root/workspace/logs/config.json"
```

\---

### 2.2 Upload index.html

#### `POST /xlabopenapi/github/aigames/index`

#### Request Parameters (form-data)

|Parameter|Type|Required|Description|
|-|-|-|-|
|`gameFolder`|string|Yes|Game folder name, must match the one used when uploading config.json|
|`file`|file|Yes|index.html main game file|

#### curl Example

```bash
curl -X POST "https://www.idlab.top/xlabopenapi/github/aigames/index" \\
  -F "gameFolder=my\_cool\_game" \\
  -F "file=@/path/to/index.html"
```

\---

### 2.3 Upload preview.png

#### `POST /xlabopenapi/github/aigames/preview`

#### Request Parameters (form-data)

|Parameter|Type|Required|Description|
|-|-|-|-|
|`gameFolder`|string|Yes|Game folder name, must match the one used when uploading config.json|
|`file`|file|Yes|preview.png game screenshot (recommended size 400×300)|

#### curl Example

```bash
curl -X POST "https://www.idlab.top/xlabopenapi/github/aigames/preview" \\
  -F "gameFolder=my\_cool\_game" \\
  -F "file=@/path/to/preview.png"
```

\---

## III. Complete Process for Uploading a New Game (AI Call Example)

> Assuming you want to upload a Snake game named `pixel\_snake`, the steps are as follows:

### Step 1: Upload config.json

```bash
curl -X POST "https://www.idlab.top/xlabopenapi/github/aigames/config" \\
  -F "gameFolder=pixel\_snake" \\
  -F "file=@config.json"
```

config.json content:

```json
{"title": "Pixel Snake"
}
```

### Step 2: Upload index.html

```bash
curl -X POST "https://www.idlab.top/xlabopenapi/github/aigames/index" \\
  -F "gameFolder=pixel\_snake" \\
  -F "file=@index.html"
```

### Step 3: Upload preview.png

```bash
curl -X POST "https://www.idlab.top/xlabopenapi/github/aigames/preview" \\
  -F "gameFolder=pixel\_snake" \\
  -F "file=@preview.png"
```

### Step 4: If successful, inform the user that the upload is complete

Provide the experience URL as https://thenext.games/game/ + gameFolder. For example, in the case above: https://thenext.games/game/pixel\_snake

\---

## IV. Common Response Structure

All interfaces return a unified structure:

```json
{
  "code": 200, // 200 indicates success, other values indicate failure
  "message": "success",
  "data": { ... } // Returned data on success
}
```

### Common Error Codes

|code|Meaning|
|-|-|
|200|Success|
|400|Parameter error (e.g., file already exists, gameFolder is empty, etc.)|
|500|Internal server error (e.g., GitHub API call failed)|

\---

## V. Important Notes

1. **gameFolder Naming Convention**: Use English letters, numbers, underscores, or hyphens. Do not use Chinese characters or spaces, e.g., `my\_cool\_game`, `pixel-snake`.
2. **Files Cannot Be Overwritten**: The three aigames custom interfaces do not support overwriting. If a file already exists, an error will be returned. To overwrite, use the general interface with `overwrite=true`.
3. **Upload Order Not Required**: The three files (config.json, index.html, preview.png) can be uploaded in any order, but it's recommended to upload config.json first.
4. **File Size Limit**: The server limits individual files to a maximum of 50MB.
5. **preview.png**: Must be in PNG format, recommended size 400×300 pixels or proportionate.

\---

I noticed there was a formatting issue in the config.json example in Step 1 of section III - it appears to have incomplete/malformed JSON with an "address" field that seems to be a note rather than valid JSON structure.

