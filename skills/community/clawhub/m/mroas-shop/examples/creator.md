# Example · Creator showcase

## User
> Show me what mom_lifestyle_us has been promoting recently — I want to see her style.

## Agent action
```bash
curl -H 'X-Moras-Skill: moras-shop' \
  'https://selltoai.ai/v1/creators/mom_lifestyle_us/showcase?limit=6&channel=cursor'
```

## Agent reply

> Here are mom_lifestyle_us's top-performing TikTok Shop products on Moras:
>
> *(rendered as 6 PCD cards using the same template as recommend.md)*
