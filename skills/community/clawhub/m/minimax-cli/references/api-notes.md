# MiniMax CLI Reference Notes

## Voice List (sample)

English voices available:
- English_expressive_narrator
- English_radiant_girl
- English_magnetic_voiced_man
- English_compelling_lady1
- English_Aussie_Bloke
- English_captivating_female1
- English_Upbeat_Woman
- English_Trustworth_Man
- English_CalmWoman
- English_UpsetGirl
- English_Gentle-voiced_man
- English_Whispering_girl
- English_Diligent_Man
- English_Graceful_Lady
- English_ReservedYoungMan
- English_PlayfulGirl
- English_ManWithDeepVoice
- English_MaturePartner
- English_FriendlyPerson

Full list: `mmx speech voices`

## Video Workflow (Async)

1. Submit job: `mmx video generate --prompt "..." --async`
2. Get task ID from response
3. Poll: `mmx video task get --task-id <id>`
4. Download when complete: `mmx video download --file-id <id> --out video.mp4`

## API Key Location

Config: `~/.mmx/config.json`
Key in env: `MINIMAX_API_KEY`

## Dual Region Support

Global endpoint: `api.minimax.io` (default)
CN endpoint: `api.minimaxi.com`

Switch: `mmx config set --key region --value cn`
