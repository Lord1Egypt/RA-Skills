# IPFS Content Gateway Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `ipfs-content-gateway`

x402 availability: not enabled for this product.

## `list`

Action slug: `list`

Price: `20` credits

List all files previously uploaded through this tool, sorted by most recent first. Returns upload history with CIDs, filenames, sizes, dates, and gateway URLs.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `retrieve`

Action slug: `retrieve`

Price: `20` credits

Fetch content from IPFS by its Content Identifier (CID). Supports both CIDv0 (Qm...) and CIDv1 (bafy...) formats. Multiple gateways are tried automatically for reliability.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cid` | `string` | yes | IPFS Content Identifier. Supports CIDv0 (Qm...) and CIDv1 (bafy...) formats. Example: 'QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG' |

Sample parameters:

```json
{
  "cid": "example cid"
}
```

Generated JSON parameter schema:

```json
{
  "cid": {
    "description": "IPFS Content Identifier. Supports CIDv0 (Qm...) and CIDv1 (bafy...) formats. Example: 'QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG'",
    "required": true,
    "type": "string"
  }
}
```

## `upload`

Action slug: `upload`

Price: `20` credits

Upload a file to IPFS. The file is pinned so it remains available on the network. Maximum file size is 10MB. Files must be base64-encoded before uploading.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | `string` | yes | Base64-encoded file content. Maximum file size: 10MB. Encode your file content as base64 before sending. |
| `filename` | `string` | yes | Original filename with extension. Example: 'document.pdf' or 'image.png' |
| `pinning_api_key` | `string` | no | Optional API key for your own pinning service (Pinata, Web3.Storage, or NFT.Storage). If not provided, shared service credentials will be used. |
| `pinning_service` | `string` | no | Pinning service to use with pinning_api_key. Required if pinning_api_key is provided. |

Sample parameters:

```json
{
  "content": "Draft marketing copy to check for banned phrases.",
  "filename": "example filename",
  "pinning_api_key": "example pinning api key",
  "pinning_service": "pinata"
}
```

Generated JSON parameter schema:

```json
{
  "content": {
    "description": "Base64-encoded file content. Maximum file size: 10MB. Encode your file content as base64 before sending.",
    "required": true,
    "type": "string"
  },
  "filename": {
    "description": "Original filename with extension. Example: 'document.pdf' or 'image.png'",
    "required": true,
    "type": "string"
  },
  "pinning_api_key": {
    "description": "Optional API key for your own pinning service (Pinata, Web3.Storage, or NFT.Storage). If not provided, shared service credentials will be used.",
    "required": false,
    "type": "string"
  },
  "pinning_service": {
    "description": "Pinning service to use with pinning_api_key. Required if pinning_api_key is provided.",
    "enum": [
      "pinata",
      "web3storage",
      "nftstorage"
    ],
    "required": false,
    "type": "string"
  }
}
```
