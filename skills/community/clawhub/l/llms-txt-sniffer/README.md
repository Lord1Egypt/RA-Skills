# llms-txt-sniffer

Sniff out `llms.txt` index files on documentation sites. Helps locate AI-friendly documentation resources fast.

## Usage

```bash
python3 sniffer.py <URL>
```

## Install

```bash
clawhub install llms-txt-sniffer
```

## Example

```bash
python3 sniffer.py https://docs.example.com
# -> {"found_index": "https://docs.example.com/llms.txt", "type": "llms.txt"}
```

> Full docs: [SKILL.md](./SKILL.md)
