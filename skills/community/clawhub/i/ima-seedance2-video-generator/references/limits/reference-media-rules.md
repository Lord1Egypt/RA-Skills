# Reference Media Rules

## Images

| Rule | Allowed |
|---|---|
| count | `1~9` |
| formats | `jpeg`, `png`, `webp`, `bmp`, `tiff`, `gif` |
| width / height | `300~6000 px` |
| aspect ratio | `0.4~2.5` |
| single file size | `< 30MB` |

## Videos

| Rule | Allowed |
|---|---|
| count | `0~3` |
| formats | `mp4`, `mov` |
| single duration | `2~15s` |
| total duration | `<= 15s` |
| width / height | `300~6000 px` |
| aspect ratio | `0.4~2.5` |
| pixels | `409600~927408` |
| fps | `24~60` |
| single file size | `<= 50MB` |

## Audio

| Rule | Allowed |
|---|---|
| count | `0~3` |
| formats | `wav`, `mp3` |
| single duration | `2~15s` |
| total duration | `<= 15s` |
| single file size | `<= 15MB` |

## Remote URL Policy

- remote URLs must be probeable before create-task
- probe failure is a stop condition

## Compliance Verification Scope

- image references: verify
- video references: verify
- audio references: verify
