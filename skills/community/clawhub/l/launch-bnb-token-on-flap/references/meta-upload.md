# Token Metadata — Upload to Flap

Token metadata is stored on IPFS and must be pinned via Flap's upload API. The Flap indexer and partner terminals serve files exclusively through the Flap gateway.

**Upload endpoint:** `https://funcs.flap.sh/api/upload`

## Metadata fields

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Token name |
| `symbol` | yes | Token ticker symbol |
| image file | yes | Any common image format (PNG recommended) |
| `description` | no | Short description |
| `twitter` | no | Twitter/X handle (without `@`) |
| `telegram` | no | Telegram group/channel link or handle |

## Upload (TypeScript with axios)

```typescript
import axios from "axios";
import fs from "fs";

const UPLOAD_API = "https://funcs.flap.sh/api/upload";

const MUTATION_CREATE = `
  mutation Create($file: Upload!, $meta: MetadataInput!) {
    create(file: $file, meta: $meta)
  }
`;

async function uploadTokenMeta(opts: {
  imagePath: string;
  description?: string;
  twitter?: string;
  telegram?: string;
  website?: string;
}): Promise<string> {
  const form = new FormData();

  form.append(
    "operations",
    JSON.stringify({
      query: MUTATION_CREATE,
      variables: {
        file: null,
        meta: {
          description: opts.description ?? "",
          twitter: opts.twitter ?? null,
          telegram: opts.telegram ?? null,
          website: opts.website ?? null,
          creator: "0x0000000000000000000000000000000000000000",
        },
      },
    })
  );

  form.append("map", JSON.stringify({ "0": ["variables.file"] }));

  const file = new File([fs.readFileSync(opts.imagePath)], "image.png", {
    type: "image/png",
  });
  form.append("0", file);

  const res = await axios.postForm(UPLOAD_API, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  if (res.status !== 200) {
    throw new Error(`Upload failed: ${res.statusText}`);
  }

  // Returns the IPFS CID string — use this as the `meta` field in the token params.
  return res.data.data.create as string;
}
```

The returned string is the IPFS CID. Store it as `meta` and use it as-is in the token launch params.
