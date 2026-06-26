# Domains

## Implemented now

### light
- device aliases: 電気, ライト, 照明
- actions:
  - on: つけて, つける, オン
  - off: 消して, けして, オフ

### aircon
- device aliases: エアコン
- actions:
  - on: つけて
  - off: 消して, 止めて, とめて
  - set_mode: にして, つけて, して
- modes:
  - cool: 冷房, れいぼう, れーぼー, れいほう, 涼しくして
  - heat: 暖房, だんぼう, だんぼー, 暖かくして
  - dry: 除湿, じょしつ, 除しつ
  - fan: 送風, そうふう, 風だけ

## Schema already prepared for expansion

### curtain
- device aliases: カーテン, ブラインド
- actions:
  - open: 開けて, あけて
  - close: 閉めて, しめて

### tv
- device aliases: テレビ, TV
- actions:
  - on: つけて
  - off: 消して

## Extension guidance

When adding a new device:
1. define device aliases
2. define actions
3. define optional slots such as mode or value
4. add fixtures before wiring execution
5. only then connect it to the actual device-control layer
