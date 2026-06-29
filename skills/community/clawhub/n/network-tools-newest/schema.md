# Network Tools Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `network-tools`

x402 availability: not enabled for this product.

## `network-binary-to-ipv4`

Action slug: `network-binary-to-ipv4`

Price: `5` credits

Convert a 32-bit binary string back to an IPv4 dotted-decimal address.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | 32-bit binary string (dots and spaces allowed, e.g., '11000000.10101000.00000001.00000001') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "32-bit binary string (dots and spaces allowed, e.g., '11000000.10101000.00000001.00000001')",
    "required": true,
    "type": "string"
  }
}
```

## `network-cidr-to-range`

Action slug: `network-cidr-to-range`

Price: `5` credits

Convert CIDR notation to a start/end IP range with sample IPs.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | CIDR notation (e.g., '192.168.1.0/28') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "CIDR notation (e.g., '192.168.1.0/28')",
    "required": true,
    "type": "string"
  }
}
```

## `network-cidr-validate`

Action slug: `network-cidr-validate`

Price: `5` credits

Validate CIDR notation, check whether it uses strict network addressing, and suggest corrections if needed.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | CIDR notation to validate (e.g., '192.168.1.100/24') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "CIDR notation to validate (e.g., '192.168.1.100/24')",
    "required": true,
    "type": "string"
  }
}
```

## `network-dns-lookup`

Action slug: `network-dns-lookup`

Price: `5` credits

Resolve a hostname to its IP address(es) including all A records.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | Hostname to resolve (e.g., 'google.com') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "Hostname to resolve (e.g., 'google.com')",
    "required": true,
    "type": "string"
  }
}
```

## `network-generate-ipv6`

Action slug: `network-generate-ipv6`

Price: `5` credits

Generate a random IPv6 address in both full and compressed notation. No input required.

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

## `network-integer-to-ipv4`

Action slug: `network-integer-to-ipv4`

Price: `5` credits

Convert an integer (0-4294967295) back to an IPv4 dotted-decimal address.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | Integer value as a string (e.g., '3232235777') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "Integer value as a string (e.g., '3232235777')",
    "required": true,
    "type": "string"
  }
}
```

## `network-ip-in-range`

Action slug: `network-ip-in-range`

Price: `5` credits

Check whether a specific IPv4 address falls within a given CIDR range.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | IPv4 address to check (e.g., '192.168.1.50') |
| `input2` | `string` | yes | CIDR notation to check against (e.g., '192.168.1.0/24') |

Sample parameters:

```json
{
  "input": "example input",
  "input2": "example input2"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "IPv4 address to check (e.g., '192.168.1.50')",
    "required": true,
    "type": "string"
  },
  "input2": {
    "description": "CIDR notation to check against (e.g., '192.168.1.0/24')",
    "required": true,
    "type": "string"
  }
}
```

## `network-ip-info`

Action slug: `network-ip-info`

Price: `5` credits

Get detailed classification information about an IPv4 address including class, private/public status, and special designations.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | IPv4 address to analyze (e.g., '10.0.0.1') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "IPv4 address to analyze (e.g., '10.0.0.1')",
    "required": true,
    "type": "string"
  }
}
```

## `network-ipv4-to-binary`

Action slug: `network-ipv4-to-binary`

Price: `5` credits

Convert an IPv4 address to its 32-bit binary representation (continuous and dotted notation).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | IPv4 address to convert (e.g., '192.168.1.1') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "IPv4 address to convert (e.g., '192.168.1.1')",
    "required": true,
    "type": "string"
  }
}
```

## `network-ipv4-to-integer`

Action slug: `network-ipv4-to-integer`

Price: `5` credits

Convert an IPv4 address to its integer and hexadecimal representations.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | IPv4 address to convert (e.g., '192.168.1.1') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "IPv4 address to convert (e.g., '192.168.1.1')",
    "required": true,
    "type": "string"
  }
}
```

## `network-mac-format`

Action slug: `network-mac-format`

Price: `5` credits

Reformat a MAC address into different notation styles (colon, dash, dot, or plain).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | MAC address in any format (e.g., '00:1A:2B:3C:4D:5E', '001A2B3C4D5E') |
| `output_format` | `string` | no | Output format style for the MAC address |

Sample parameters:

```json
{
  "input": "example input",
  "output_format": "colon"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "MAC address in any format (e.g., '00:1A:2B:3C:4D:5E', '001A2B3C4D5E')",
    "required": true,
    "type": "string"
  },
  "output_format": {
    "default": "colon",
    "description": "Output format style for the MAC address",
    "enum": [
      "colon",
      "dash",
      "dot",
      "plain"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `network-port-validate`

Action slug: `network-port-validate`

Price: `5` credits

Validate a port number and identify the associated well-known service (e.g., HTTP, SSH, MySQL).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | Port number as a string (1-65535, e.g., '443') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "Port number as a string (1-65535, e.g., '443')",
    "required": true,
    "type": "string"
  }
}
```

## `network-private-ip-check`

Action slug: `network-private-ip-check`

Price: `5` credits

Check whether an IPv4 address belongs to a private (RFC 1918), loopback, or link-local range, and identify the specific range.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | IPv4 address to check (e.g., '172.16.5.10') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "IPv4 address to check (e.g., '172.16.5.10')",
    "required": true,
    "type": "string"
  }
}
```

## `network-reverse-dns`

Action slug: `network-reverse-dns`

Price: `5` credits

Perform a reverse DNS lookup on an IPv4 address to find its associated hostname (PTR record).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | IPv4 address to look up (e.g., '8.8.8.8') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "IPv4 address to look up (e.g., '8.8.8.8')",
    "required": true,
    "type": "string"
  }
}
```

## `network-subnet-calculator`

Action slug: `network-subnet-calculator`

Price: `5` credits

Calculate full subnet details from CIDR notation including network/broadcast addresses, netmask, wildcard, usable hosts, and IP class.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `input` | `string` | yes | CIDR notation (e.g., '192.168.1.0/24') |

Sample parameters:

```json
{
  "input": "example input"
}
```

Generated JSON parameter schema:

```json
{
  "input": {
    "description": "CIDR notation (e.g., '192.168.1.0/24')",
    "required": true,
    "type": "string"
  }
}
```
