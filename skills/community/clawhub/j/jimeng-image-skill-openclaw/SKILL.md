---
name: "Jimeng-Image"

description: "Use Python to send an image prompt to the Jimeng API and retrieve the generated image from the response when user says "generate image ..."
---

# Jimeng-Image

## When to use this skill

Use this skill when user express "You need generate a image".

## How to use this skill

1. You need putAccess Key and Secret Key via either environment variable: `Jimeng_Secret_Key` and  ` Jimeng_Access_Key=...`, or`~/.openclaw/.env` line: `Jimeng_Secret_Key=...` and ` Jimeng_Access_Key=...`   on your environment variable.

2. You need to  execute scripts/main.py
3. When the response is arrive, the script will save the png file on ~/.openclaw/workspace/images. (The script will create images dir if the images  dir is not exist)
4. Finally, you need send the new image to user by same channel,such as qqbot etc. from  ~/.openclaw/workspace/images

## Requirement

- argparse
- datetime
- volcengine-python-sdk
- base64
- os

If not exits ,you need pip it.

## Tips: 

- the baseDir is your workspace /skills/Jimeng-Image
- If the user does not specify the output path,the output dir is ~/.openclaw/workspace/images

## Command example 

**user**:

​	i need a image by prompt:"A girl in an anime style"

**You**: 

​	Run from the OpenClaw workspace:

```sh
 python3 {baseDir}/scripts/main.py --prompt "A girl in an anime style"
```



**user**:

​	i need a image by prompt:"A girl in an anime style and width is 512 and height is 512"

**You**:

​	Run from the OpenClaw workspace:

```
python3 {baseDir}/scripts/main.py --prompt "A girl in an anime style" --width "512" --height "512"
```



## The Script command line parameter

| 参数            | 类型    | 默认值                           | 说明                                        |
| :-------------- | :------ | :------------------------------- | :------------------------------------------ |
| `--prompt`      | `str`   | `'none'`                         | Path of the prompt file                     |
| `--output_path` | `str`   | `'~/.openclaw/workspace/images'` | The saving path of the output file          |
| `--use_pre_llm` | `bool`  | `False`                          | Whether to use a pre-trained language model |
| `--seed`        | `int`   | `-1`                             | Random seed ( `-1` indicates random )       |
| `--scale`       | `float` | `1.0`                            | The scaling ratio of the output image       |
| `--width`       | `int`   | `1920`                           | The width (in pixels) of the output image   |
| `--height`      | `int`   | `1080`                           | The height (in pixels) of the output image  |



