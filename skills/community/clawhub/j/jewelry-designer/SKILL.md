---
name: "jewelry-designer"
description: "Agentic AI Jewelry Designer generates hand-drawn design sheets, multiview sketches, and interactive 3D jewelry online viewers from your ideas and reference images. Customize designs using gemstone images, gemstone types, metals, shapes, and materials. Supports luxury bracelets, beaded bracelets, necklaces, rings, anklets, body chains, pet collars, earrings, charms, pendants, chokers, and more."
env:
  DEEPNLP_ONEKEY_ROUTER_ACCESS:
    required: true
    description: OneKey Gateway Registered API and Usage access key
dependencies:
  node: []
  python: []
---

# AI Jewelry Designer Skills from Craftsman Agent

The AI Jewelry Designer workflow generates jewelry concepts, hand-drawn design sheets, multiview reference sheets, and interactive 3D models. The Jewelry Designer APIs are served through the OneKey Agent Gateway and used by the Craftsman Agent Jewelry Designer website:

https://craftsman-agent.aiagenta2z.com/app/jewelry-designer


#### Demo: Hand Drawn Jewelry Images:

prompt: Ruby Ring Design Oval Cut

Hand Drawn Style Image: 

<img src="https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/d426ff6f-bd56-49d1-9ec9-54906bcc78bd.png" alt="Craftsman-agent Agentic Jewelry Designer Ring" width="500" />

#### Demo: Online 3D interactive Ring Designer:
prompt: Sapphire Ring with twisted Band, US Size 10
[3d online ring interactive viewer](https://craftsman-agent.aiagenta2z.com/app/sessions/share/45c9f495-3f14-4093-bcef-5f85d6910a3a)


The typical jewelry designer workflow include:

```commandline
[Text/Image Prompt of your Preferred Gems, Metals, Styles]
        ->
[Jewelry Design Hand-Drawn Design  / Multi-View Sheet]
        ->
[Jewelry Design 3D Generation Interactive Viewers]
        or
[Jewelry Design 3D Models]        
        ->
[Preview]
        ->
[Manufacturing on Demand Send Designs to Factory]
```

| API                        | Description                                                                                                                          |
| ------------------------------ |--------------------------------------------------------------------------------------------------------------------------------------|
| jewelry_generator_design_draft | Generate Design Draft of your Prefered Gem Stones Images and Prompts on 1000+ Jewerly typical design patterns                        |
| jewelry_generator_hand_drawn_sketch | Generate Hand-Drawn Style Sketch Draft of your Prefered Gem Stones Images and Prompts on 1000+ Jewerly typical design patterns |


### OneKey Agent Gateway

The Jewelry Designer APIs are registered under:
unique_id: craftsman-agent/craftsman-agent
Gateway endpoint:
```commandline
https://agent.deepnlp.org/agent_router

```
Set the registered OneKey Gateway access key:

```
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

| Section                                 | Description                                                 |
|-----------------------------------------|-------------------------------------------------------------|
| Craftsman Jewelry Designer App Online   | https://craftsman-agent.aiagenta2z.com/app/jewelry-designer |
| Craftsman Website                       | https://craftsman-agent.aiagenta2z.com                      |
| Craftsman App                           | https://craftsman-agent.aiagenta2z.com/app                  |
| Craftsman Gallery                       | https://craftsman-agent.aiagenta2z.com/gallery              |
| Craftsman Workspace                     | https://craftsman-agent.aiagenta2z.com/workspace            |
| Craftsman Marketplace                   | https://craftsman-agent.aiagenta2z.com/marketplace          |
| Craftsman Manufacturing on Demand Store | https://craftsman-agent.aiagenta2z.com/store                |


## Quick Start
Set the registered OneKey Gateway access key `DEEPNLP_ONEKEY_ROUTER_ACCESS` from AI Agent Marketplace at the [Website](https://www.deepnlp.org/workspace/keys).

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

### Prompt Examples:

####  Template ID: bracelet

  Prompt: Design a nice bracelet of Clover shapes. The chain should use rose gold and gem is white mother of pearl color.

####  Template ID: beaded-bracelet

  Prompt: Beaded Bracelet Chain of Aqua stones

####  Template ID: ring

  Prompt: Create an 18K Yellow Gold ring featuring a diamond with a 6-prong setting.

####  Template ID: necklace

  Prompt: Design a platinum rope chain necklace with a heart-shaped pendant.

####  Template ID: pet-jewelry-collar

  Prompt: Make a leather cat collar with a synthetic ruby main stone.

####  Template ID: earrings

  Prompt: Silver hoop earrings adorned with cubic zirconia stones.

####  Template ID: body-chain

  Prompt: Design a gold waist chain decorated with crystals.


# 1. API: Jewelry Generator Design Draft

### 1.1 REST API Requests Usage
```
jewelry_generator_design_draft
```
Generate a jewelry design draft from text prompts, gemstone/reference images, and structured jewelry parameters.

The design draft can contain a online 3D jewelry model viewers available to choose each instance on the interactive 3ds for future modification.

#### Requests Input Parameter

| Parameter         | Description                                                                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| prompt            | Text description of the desired jewelry design                                                                                                  |
| images            | Array of source image URLs used as visual references, including gemstone images                                                                 |
| template_id       | Jewelry category templates including `bracelet`, `beaded-bracelet`, `ring`, `necklace`, `pet-jewelry-collar`, `earrings`, `body-chain` and more |
| options           | Structured jewelry customization parameters defined by the selected templates                                                                   |
| provider_model_id | Jewelry design provider/model identifier; `default` is supported                                                                                |
| session_name      | Name of the generated workspace session                                                                                                         |
| tag_list          | Optional tags associated with the generation                                                                                                    |
| mode              | Generation mode such as `basic`, `standard`, `advanced`, or `demo`                                                                              |



#### Input Parameter Options

**template_id**: The template of the jewelry to generate

#### Supported Jewelry Category Template IDs

Supported `template_id` include

| Template ID        | Jewelry Type              | Description                                                                                 |
|--------------------| ------------------------- |---------------------------------------------------------------------------------------------|
| bracelet           | Bracelet                  | Gems, Chain, bangle, cuff, tennis, charm, beaded, stretch, and wrap bracelets               |
| beaded-bracelet    | Beaded Bracelet           | Gems, Crystal, natural stone, pearl, wooden, glass, charm, stretch, and layered bracelets   |
| ring               | Ring                      | Classic, wedding band, engagement, signet, stackable, eternity, cocktail, and fashion rings |
| necklace           | Necklace                  | Chain, pendant, layered, statement, tennis, pearl, lariat, and locket necklaces             |
| pet-jewelry-collar | Pet Jewelry & Collar      | Custom jewelry collars for dogs, cats, rabbits, and small animals                           |
| earrings           | Earrings                  | Stud, hoop, huggie, drop, dangle, chandelier, and ear-cuff earrings                         |
| body-chain         | Body Chain & Body Jewelry | Waist, belly, breast, body, harness, chest, back, and thigh chains                          |


**mode**: The mode as complexity of design for each generation task

| mode     | Description                                                                                                           |
|----------|-----------------------------------------------------------------------------------------------------------------------|
| basic    | Basic Complexity for Design                                                                                           |
| standard | Standard Complexity for Design                                                                                        |
| advanced | Advanced Complexity for Design                                                                                        |
| demo     | Demo mode will only return predefined results for debug and APIs purposes, for production, please use other settings. |

#### Requests Input Example
```commandline
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
  -H "Content-Type: application/json" \
  -H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
  -d '{
    "unique_id": "craftsman-agent/craftsman-agent",
    "api_id": "jewelry_generator_design_draft",
    "data": {
      "prompt": "Crystl Beaded Bracelet Chain of 12 Aqua stones",
      "images": [],
      "template_id": "beaded-bracelet",
      "provider_model_id": "default",
      "options": {},
      "session_name": "Jewelry Design",
      "tag_list": "",
      "mode": "demo"
    }
  }'

```

This example use the demo mode for debug purpose, for real example, please use 'basic' instead.


#### Output Keys Definition
| Key                  | Description                                                             |
|----------------------|-------------------------------------------------------------------------|
| success              | Whether the design draft generation succeeded                           |
| share_url            | The URL of workspace containing the canvas to view the design           |
| blueprint            | Jewelry design blueprint data, when available                               |
| reference_images     | Generated reference image URLs                                          |
| final_image_url      | URL of the generated multi-view design sheet                            |
| options              | The options AI designer generated to display on the base jewelry models |
| session_id           | Workspace/session identifier                                            |
| title                | Generated session title                                                 |
| workspace_session_id | Workspace session identifier                                            |
| tag_list             | Tags associated with the generation                                     |


#### Output Example
```commandline
{
  "success": true,
  "blueprint": {},
  "reference_images": [],
  "final_image_url": "",
  "overall_image": {},
  "session_id": "31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb",
  "title": "Jewelry Designer Crystal Beaded Bracelet Chain White Mother of Pearl",
  "workspace_session_id": "",
  "tag_list": "",
  "options": {
     "count": 15,
     "material": "aqua"
  },
  "prompt": "Crystal Beaded Bracelet Chain of 12 Aqua stones",
  "share_url": "https://craftsman-agent.aiagenta2z.com/app/sessions/share/31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb?pwd=de06"
}
```


**Note**:
`share_url`: After the Jewelry Design generation task finished, a `share_url` value contains URL of the canvas workspace will be returned.
This is the website to view the progress of the generation and the multiview sheets, the front view, side view, backview.
Please notify user the `share_url` link to view the Jewelry Design generation task status and results online!


### 1.2 CLI Usage

```shell
npx onekey agent craftsman-agent/craftsman-agent jewelry_generator_design_draft '{"prompt":"Crystal Beaded Bracelet Chain of 12 Aqua stones","images":[],"template_id":"beaded-bracelet","provider_model_id":"default","options":{},"session_name":"Jewelry Design","tag_list":"","mode":"demo"}'
```


#### 1.3 Detailed Jewelry Designer Options

#### 1.3.1 Bracelet

`template_id`: `bracelet`

### Main Parameters

  -----------------------------------------------------------------------
  Parameter                           Supported IDs / Value
  ----------------------------------- -----------------------------------
  `wrist_circumference`               Default `18cm`

  `bracelet_length`                   Default `18cm`

  `width`                             Default `5mm`

  `thickness`                         Default `3mm`

  `chain_type`                        `cuban`, `figaro`, `rope`,
                                      `paperclip`, `box`, `snake`

  `surface_finish`                    `polished`, `matte`, `brushed`,
                                      `hammered`, `plated`

  `clasp_type`                        `lobster`, `toggle`, `magnetic`,
                                      `buckle`, `spring-ring`

  `gemstone_type`                     `none`, `carnelian`, `onyx`,
                                      `motherofpearl`, `malachite`,
                                      `diamond`, `crystal`, `pearl`

  `layer_count`                       `1`, `2`, `3`

  `adjustability`                     `fixed`, `adjustable`

  `material`                          `default`, `yellow-gold`,
                                      `white-gold`, `rose-gold`,
                                      `silver`, `platinum`,
                                      `stainless-steel`, `leather`,
                                      `beads`

  `asset_size`                        `default`, `small`, `medium`,
                                      `large`
  -----------------------------------------------------------------------

### Sub Categories

`sub_category`: `chain`, `bangle`, `cuff`, `tennis`, `charm`, `beaded`, `stretch`, `wrap`

### Parameter Metadata

  -----------------------------------------------------------------------
  Parameter               ID                      Metadata
  ----------------------- ----------------------- -----------------------
  `asset_size`            `small`                 `width`=`16cm`,
                                                  `height`=`5mm`,
                                                  `depth`=`3mm`,
                                                  `unit`=`cm`

  `asset_size`            `medium`                `width`=`18cm`,
                                                  `height`=`7mm`,
                                                  `depth`=`4mm`,
                                                  `unit`=`cm`

  `asset_size`            `large`                 `width`=`21cm`,
                                                  `height`=`10mm`,
                                                  `depth`=`5mm`,
                                                  `unit`=`cm`
  -----------------------------------------------------------------------


## 1.3.2. Beaded Bracelet

`template_id`: `beaded-bracelet`

### Main Parameters

  -----------------------------------------------------------------------
  Parameter                           Supported IDs / Value
  ----------------------------------- -----------------------------------
  `asset_size`                        `default`, `small`, `medium`,
                                      `large`

  `wrist_circumference`               Default `18cm`

  `bracelet_length`                   Default `18cm`

  `bead_shape`                        `round`, `faceted`, `oval`,
                                      `barrel`, `cube`, `disc`, `bicone`,
                                      `irregular`, `custom`

  `bead_size`                         `4mm`, `6mm`, `8mm`, `10mm`,
                                      `12mm`, `14mm`, `custom`

  `bead_count`                        `15`, `18`, `20`, `22`, `24`,
                                      `custom`

  `bead_color`                        `clear`, `white`, `black`, `pink`,
                                      `purple`, `blue`, `green`, `red`,
                                      `yellow`, `mixed`, `custom`

  `bead_pattern`                      `single-color`, `alternating`,
                                      `gradient`, `random`,
                                      `symmetrical`, `center-accent`

  `material`                          `clear`, `amethyst`, `rose`,
                                      `citrine`, `smoky`, `aqua`, `moon`,
                                      `lab`, `straw`, `rutile`,
                                      `phantom`, `sunstone`, `obsidian`,
                                      `tiger`, `agate`, `jade`,
                                      `emerald`, `ruby`, `sapphire`,
                                      `lapis`, `garnet`, `topaz`,
                                      `amazon`, `kunzite`, `pearl`

  `gemstone_type`                     `none`, `amethyst`, `rose-quartz`,
                                      `clear-quartz`, `smoky-quartz`,
                                      `citrine`, `agate`, `jade`,
                                      `obsidian`, `tiger-eye`,
                                      `lapis-lazuli`, `turquoise`,
                                      `tourmaline`, `mixed`

  `string_type`                       `elastic`, `nylon`, `silicone`,
                                      `wire`, `leather`

  `string_color`                      `clear`, `white`, `black`, `brown`,
                                      `gold`, `silver`, `custom`

  `accent_beads`                      `none`, `gold`, `silver`, `pearl`,
                                      `crystal`, `metal`

  `center_bead`                       `none`, `large-bead`, `charm`,
                                      `pendant`, `engraved`

  `charm_type`                        `none`, `heart`, `star`, `flower`,
                                      `animal`, `letter`, `symbol`,
                                      `custom`

  `layer_count`                       `1`, `2`, `3`

  `closure`                           `stretch`, `lobster`, `toggle`,
                                      `magnetic`, `buckle`

  `adjustability`                     `fixed`, `adjustable`
  -----------------------------------------------------------------------

### Sub Categories

`sub_category`: `crystal-beaded`, `natural-stone`, `pearl`,
`wooden-beaded`, `glass-beaded`, `charm-beaded`, `stretch`, `layered`

### Parameter Metadata

  -----------------------------------------------------------------------
  Parameter               ID                      Metadata
  ----------------------- ----------------------- -----------------------
  `asset_size`            `small`                 `width`=`16cm`,
                                                  `height`=`6mm`,
                                                  `depth`=`6mm`,
                                                  `unit`=`cm`

  `asset_size`            `medium`                `width`=`18cm`,
                                                  `height`=`8mm`,
                                                  `depth`=`8mm`,
                                                  `unit`=`cm`

  `asset_size`            `large`                 `width`=`21cm`,
                                                  `height`=`10mm`,
                                                  `depth`=`10mm`,
                                                  `unit`=`cm`
  -----------------------------------------------------------------------

## 1.3.3 Ring

`template_id`: `ring`

### Main Parameters

  -----------------------------------------------------------------------
  Parameter                           Supported IDs / Value
  ----------------------------------- -----------------------------------
  `ring_size`                         `us-3`, `us-4`, `us-5`, `us-6`,
                                      `us-7`, `us-8`, `us-9`, `us-10`,
                                      `us-11`, `us-12`, `us-13`, `custom`

  `ring_face_width`                   Default `8mm`

  `ring_thickness`                    Default `2mm`

  `band_shape`                        `classic`, `flat`, `knife`,
                                      `twist`, `pave`

  `band_metal`                        `silver`, `white`, `gold`, `rose`,
                                      `platinum`, `black`

  `surface_finish`                    `polished`, `brushed`, `matte`,
                                      `satin`, `hammered`, `oxidized`,
                                      `plated`

  `gem_stone`                         `none`, `diamond`, `sapphire`,
                                      `ruby`, `emerald`, `pearl`,
                                      `crystal`, `cz`

  `gem_shape`                         `round`, `oval`, `cushion`,
                                      `princess`, `emerald`, `baguette`,
                                      `marquise`, `pear`, `heart`,
                                      `cabochon`

  `gemstone_quantity`                 `none`, `one`, `three`, `five`,
                                      `ten`, `twenty`, `fifty`

  `gem_size`                          Default `9`

  `band_width`                        Default `2`

  `band_thickness`                    Default `2`

  `setting_style`                     `prong4`, `prong6`, `prong8`,
                                      `bezel`

  `engraving`                         `none`, `text`, `initials`, `date`,
                                      `symbol`

  `engraving_content`                 Default
                                      \``| |`bg_theme`| Default`black\`
  -----------------------------------------------------------------------

### Sub Categories

`sub_category`: `classic`, `wedding-band`, `engagement`, `signet`,
`stackable`, `eternity`, `cocktail`, `fashion`

### Parameter Metadata

  Parameter     ID         Metadata
  ------------- ---------- ---------------------------
  `ring_size`   `us-3`     `inner_diameter`=`14.1mm`
  `ring_size`   `us-4`     `inner_diameter`=`14.9mm`
  `ring_size`   `us-5`     `inner_diameter`=`15.7mm`
  `ring_size`   `us-6`     `inner_diameter`=`16.5mm`
  `ring_size`   `us-7`     `inner_diameter`=`17.3mm`
  `ring_size`   `us-8`     `inner_diameter`=`18.2mm`
  `ring_size`   `us-9`     `inner_diameter`=`19.0mm`
  `ring_size`   `us-10`    `inner_diameter`=`19.8mm`
  `ring_size`   `us-11`    `inner_diameter`=`20.6mm`
  `ring_size`   `us-12`    `inner_diameter`=`21.4mm`
  `ring_size`   `us-13`    `inner_diameter`=`22.2mm`
  `ring_size`   `custom`   `inner_diameter`=`Custom`

## 1.3.4 Necklace

`template_id`: `necklace`

### Main Parameters

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Parameter                           Supported IDs / Value
  ----------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  `material`                          `default`, `yellow-gold`, `white-gold`, `rose-gold`, `silver`, `platinum`, `stainless-steel`, `titanium`, `brass`

  `asset_size`                        `default`, `short`, `medium`, `long`

  `length`                            `14in`, `16in`, `18in`, `20in`, `22in`, `24in`, `30in`, `custom`

  `custom_length`                     Default `45.72`

  `chain_width`                       Default `2mm`

  `chain_type`                        `cable`, `box`, `rope`, `figaro`, `cuban`, `paperclip`, `snake`, `curb`

  `pendant`                           `none`, `single`, `multiple`

  `pendant_style`                     `heart`, `cross`, `circle`, `flower`, `letter`, `animal`, `geometric`, `custom`

  `pendant_size`                      Default `20mm`

  `clasp_type`                        `lobster`, `spring-ring`, `magnetic`, `toggle`, `hook`

  `layer_count`                       `1`, `2`, `3`, `4`, `5`

  `engraving`                         `none`, `text`, `initial`, `date`, `symbol`

  `engraving_content`                 Default
                                      \``| |`gemstone_type`|`clear`,`amethyst`,`rose`,`citrine`,`smoky`,`aqua`,`moon`,`lab`,`straw`,`rutile`,`phantom`,`sunstone`,`obsidian`,`tiger`,`agate`,`jade`,`emerald`,`ruby`,`sapphire`,`lapis`,`garnet`,`topaz`,`amazon`,`kunzite`,`pearl`| |`facet_level`|`low`,`medium`,`high\`
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Sub Categories

`sub_category`: `chain-necklace`, `pendant-necklace`,
`layered-necklace`, `statement`, `tennis`, `pearl`, `lariat`, `locket`

### Parameter Metadata

  ----------------------------------------------------------------------------------
  Parameter               ID                      Metadata
  ----------------------- ----------------------- ----------------------------------
  `asset_size`            `short`                 `width`=`40cm`, `height`=`2cm`,
                                                  `depth`=`2mm`, `unit`=`cm`

  `asset_size`            `medium`                `width`=`50cm`, `height`=`3cm`,
                                                  `depth`=`2mm`, `unit`=`cm`

  `asset_size`            `long`                  `width`=`70cm`, `height`=`4cm`,
                                                  `depth`=`2mm`, `unit`=`cm`

  `length`                `14in`                  `length_international`=`35.56cm`

  `length`                `16in`                  `length_international`=`40.64cm`

  `length`                `18in`                  `length_international`=`45.72cm`

  `length`                `20in`                  `length_international`=`50.80cm`

  `length`                `22in`                  `length_international`=`55.88cm`

  `length`                `24in`                  `length_international`=`60.96cm`

  `length`                `30in`                  `length_international`=`76.20cm`

  `length`                `custom`                `length_international`=`Custom`
  ----------------------------------------------------------------------------------

## 1.3.5 Pet Jewelry & Collar

`template_id`: `pet-jewelry-collar`

### Parameters

  -----------------------------------------------------------------------
  Parameter                           Supported IDs / Value
  ----------------------------------- -----------------------------------
  `pet_type`                          `dog`, `cat`, `rabbit`,
                                      `small-animal`

  `neck_circumference`                Default `35cm`

  `collar_width`                      Default `20mm`

  `material`                          `default`, `leather`, `nylon`,
                                      `metal`, `silicone`, `fabric`,
                                      `vegan-leather`

  `asset_size`                        `default`, `small`, `medium`,
                                      `large`

  `material_color`                    Default `Custom`

  `closure`                           `buckle`, `snap`, `quick-release`,
                                      `magnetic`

  `adjustability`                     `fixed`, `adjustable`

  `d_ring`                            `yes`, `no`

  `pet_tag`                           `yes`, `no`

  `tag_shape`                         `circle`, `bone`, `heart`,
                                      `shield`, `custom`

  `tag_size`                          Default `30mm`

  `engraving`                         `name`, `phone`, `custom-text`

  `decorative_elements`               `none`, `studs`, `charms`,
                                      `crystals`, `pearls`

  `safety_feature`                    `standard`, `reflective`,
                                      `breakaway`

  `main_stone`                        `none`, `human-made-ruby`,
                                      `human-made-sapphire`,
                                      `human-made-emerald`, `diamond`

  `side_decorations`                  `none`, `pearl`, `gold-stud`,
                                      `silver-stud`

  `side_decor_size`                   `small`, `medium`, `large`

  `main_stone_size`                   `small`, `medium`, `large`

  `decoration_layout`                 `front-and-sides`, `front-only`,
                                      `sides-only`, `symmetric`
  -----------------------------------------------------------------------

### Parameter Metadata

  -----------------------------------------------------------------------
  Parameter               ID                      Metadata
  ----------------------- ----------------------- -----------------------
  `asset_size`            `small`                 `width`=`25cm`,
                                                  `height`=`15mm`,
                                                  `depth`=`5mm`,
                                                  `unit`=`cm`

  `asset_size`            `medium`                `width`=`40cm`,
                                                  `height`=`20mm`,
                                                  `depth`=`6mm`,
                                                  `unit`=`cm`

  `asset_size`            `large`                 `width`=`55cm`,
                                                  `height`=`30mm`,
                                                  `depth`=`7mm`,
                                                  `unit`=`cm`
  -----------------------------------------------------------------------

## 1.3.6 Earrings

`template_id`: `earrings`

### Main Parameters

  -----------------------------------------------------------------------
  Parameter                           Supported IDs / Value
  ----------------------------------- -----------------------------------
  `motif_shape`                       `clover`, `butterfly`, `flower`,
                                      `heart`, `star`, `round`

  `material`                          `default`, `yellow-gold`,
                                      `white-gold`, `rose-gold`,
                                      `silver`, `platinum`,
                                      `stainless-steel`, `titanium`

  `asset_size`                        `default`, `small`, `medium`,
                                      `large`

  `diameter`                          Default `20mm`

  `drop_length`                       Default `30mm`

  `width`                             Default `5mm`

  `thickness`                         Default `2mm`

  `surface_finish`                    `polished`, `matte`, `brushed`,
                                      `satin`, `hammered`, `plated`

  `gemstone_type`                     `none`, `clear`, `amethyst`,
                                      `rose`, `citrine`, `smoky`, `aqua`,
                                      `moon`, `lab`, `straw`, `rutile`,
                                      `phantom`, `sunstone`, `obsidian`,
                                      `tiger`, `agate`, `jade`,
                                      `emerald`, `ruby`, `sapphire`,
                                      `lapis`, `garnet`, `topaz`,
                                      `amazon`, `kunzite`, `pearl`,
                                      `diamond`, `cz`

  `gemstone_quantity`                 `none`, `one`, `three`, `five`,
                                      `ten`, `twenty`, `fifty`

  `gem_cut`                           `round`, `oval`, `pear`,
                                      `marquise`, `emerald`, `princess`,
                                      `cushion`, `trillion`

  `closure`                           `push-back`, `screw-back`,
                                      `lever-back`, `hook`, `clip-on`

  `post_length`                       Default `10mm`

  `pair_quantity`                     `single`, `pair`, `set`

  `design_style`                      `minimalist`, `geometric`,
                                      `floral`, `vintage`, `luxury`,
                                      `statement`

  `engraving`                         Structured object; see details
                                      below.

  `engraving_icon`                    `none`, `heart`, `star`, `flower`,
                                      `infinity`, `moon`, `cross`,
                                      `clover`

  `engraving_font`                    `serif`, `script`, `sans`

  `stones`                            
  -----------------------------------------------------------------------

### Sub Categories

`sub_category`: `stud`, `hoop`, `huggie`, `drop`, `dangle`,
`chandelier`, `ear-cuff`

### `engraving` object

-   `enabled`: `true`
-   `initial`: `M`
-   `name`: \`\`
-   `icon`: `none`, `heart`, `star`, `flower`, `infinity`, `moon`,
    `cross`, `clover`
-   `font`: `serif`, `script`, `sans`

### Parameter Metadata

  -----------------------------------------------------------------------
  Parameter               ID                      Metadata
  ----------------------- ----------------------- -----------------------
  `asset_size`            `small`                 `width`=`8mm`,
                                                  `height`=`8mm`,
                                                  `depth`=`2mm`,
                                                  `unit`=`mm`

  `asset_size`            `medium`                `width`=`20mm`,
                                                  `height`=`20mm`,
                                                  `depth`=`3mm`,
                                                  `unit`=`mm`

  `asset_size`            `large`                 `width`=`40mm`,
                                                  `height`=`50mm`,
                                                  `depth`=`4mm`,
                                                  `unit`=`mm`
  -----------------------------------------------------------------------

## 1.3.7 Body Chain & Body Jewelry

`template_id`: `body-chain`

### Parameters

  -----------------------------------------------------------------------
  Parameter                           Supported IDs / Value
  ----------------------------------- -----------------------------------
  `body_jewelry_type`                 `waist-chain`, `belly-chain`,
                                      `breast-chain`, `body-chain`,
                                      `harness`, `chest-chain`,
                                      `back-chain`, `thigh-chain`

  `coverage_area`                     `waist`, `chest`, `shoulder`,
                                      `back`, `hip`, `thigh`, `full-body`

  `body_size`                         `xs`, `s`, `m`, `l`, `xl`, `custom`

  `chain_length`                      Default `90cm`

  `chain_width`                       Default `2mm`

  `chain_type`                        `cable`, `cuban`, `rope`,
                                      `paperclip`, `fine-chain`

  `layer_count`                       `1`, `2`, `3`, `5`

  `surface_finish`                    `polished`, `matte`, `plated`,
                                      `oxidized`

  `decorative_elements`               `none`, `charms`, `pearls`,
                                      `crystals`, `beads`

  `gemstone_type`                     `none`, `clear`, `amethyst`,
                                      `rose`, `citrine`, `smoky`, `aqua`,
                                      `moon`, `lab`, `straw`, `rutile`,
                                      `phantom`, `sunstone`, `obsidian`,
                                      `tiger`, `agate`, `jade`,
                                      `emerald`, `ruby`, `sapphire`,
                                      `lapis`, `garnet`, `topaz`,
                                      `amazon`, `kunzite`, `pearl`,
                                      `diamond`, `cz`

  `attachment`                        `hook`, `clasp`, `adjustable-chain`

  `material`                          `default`, `gold`, `yellow-gold`,
                                      `white-gold`, `rose-gold`,
                                      `silver`, `stainless-steel`,
                                      `brass`

  `asset_size`                        `default`, `small`, `medium`,
                                      `large`
  -----------------------------------------------------------------------

### Parameter Metadata

  -----------------------------------------------------------------------
  Parameter               ID                      Metadata
  ----------------------- ----------------------- -----------------------
  `asset_size`            `small`                 `width`=`70cm`,
                                                  `height`=`40cm`,
                                                  `depth`=`2mm`,
                                                  `unit`=`cm`

  `asset_size`            `medium`                `width`=`90cm`,
                                                  `height`=`50cm`,
                                                  `depth`=`2mm`,
                                                  `unit`=`cm`

  `asset_size`            `large`                 `width`=`110cm`,
                                                  `height`=`70cm`,
                                                  `depth`=`3mm`,
                                                  `unit`=`cm`
  -----------------------------------------------------------------------

------------------------------------------------------------------------


# 2. API: Jewelry Generator Hand Drawn Sketch

### 2.1 REST API Requests Usage
```
jewelry_generator_hand_drawn_sketch
```
Generate a jewelry hand-drawn style design draft from text prompts, gemstone/reference images, and structured jewelry parameters like a professional jewelry designer.

The design draft can contain the hand drawn image of gems (for example, ruby), multi-view styles sheets, gem cut, gem gallery and design text prompts.

#### Requests Input Parameter

| Parameter         | Description                                                                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| prompt            | Text description of the desired jewelry design                                                                                                  |
| images            | Array of source image URLs used as visual references, including gemstone images                                                                 |
| template_id       | Jewelry category templates including `bracelet`, `beaded-bracelet`, `ring`, `necklace`, `pet-jewelry-collar`, `earrings`, `body-chain` and more |
| options           | Structured jewelry customization parameters defined by the selected templates                                                                   |
| provider_model_id | Jewelry design provider/model identifier; `default` is supported                                                                                |
| session_name      | Name of the generated workspace session                                                                                                         |
| tag_list          | Optional tags associated with the generation                                                                                                    |
| mode              | Generation mode such as `basic`, `standard`, `advanced`, or `demo`                                                                              |


#### Example Prompt 

prompt : Rudy ring design with Oval Cut
Hand-Drawn Ruby images: https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/d426ff6f-bd56-49d1-9ec9-54906bcc78bd.png
Hand-Drawn Ruby workspace: https://craftsman-agent.aiagenta2z.com/app/sessions/share/45c9f495-3f14-4093-bcef-5f85d6910a3a

#### Requests Input Parameter

| Parameter         | Description                                                                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| prompt            | Text description of the desired jewelry design                                                                                                  |
| images            | Array of source image URLs used as visual references, including gemstone images                                                                 |
| template_id       | Jewelry category templates including `bracelet`, `beaded-bracelet`, `ring`, `necklace`, `pet-jewelry-collar`, `earrings`, `body-chain` and more |
| options           | Structured jewelry customization parameters defined by the selected templates                                                                   |
| provider_model_id | Jewelry design provider/model identifier; `default` is supported                                                                                |
| session_name      | Name of the generated workspace session                                                                                                         |
| tag_list          | Optional tags associated with the generation                                                                                                    |
| mode              | Generation mode such as `basic`, `standard`, `advanced`, or `demo`                                                                              |


#### Input Parameter Options

Supported `template_id` include

| Template ID        | Jewelry Type              | Description                                                                                 |
|--------------------| ------------------------- |---------------------------------------------------------------------------------------------|
| bracelet           | Bracelet                  | Gems, Chain, bangle, cuff, tennis, charm, beaded, stretch, and wrap bracelets               |
| beaded-bracelet    | Beaded Bracelet           | Gems, Crystal, natural stone, pearl, wooden, glass, charm, stretch, and layered bracelets   |
| ring               | Ring                      | Classic, wedding band, engagement, signet, stackable, eternity, cocktail, and fashion rings |
| necklace           | Necklace                  | Chain, pendant, layered, statement, tennis, pearl, lariat, and locket necklaces             |
| pet-jewelry-collar | Pet Jewelry & Collar      | Custom jewelry collars for dogs, cats, rabbits, and small animals                           |
| earrings           | Earrings                  | Stud, hoop, huggie, drop, dangle, chandelier, and ear-cuff earrings                         |
| body-chain         | Body Chain & Body Jewelry | Waist, belly, breast, body, harness, chest, back, and thigh chains                          |

**mode**: The mode as complexity of design for each generation task

| mode     | Description                                                                                                           |
|----------|-----------------------------------------------------------------------------------------------------------------------|
| basic    | Basic Complexity for Design                                                                                           |
| standard | Standard Complexity for Design                                                                                        |
| advanced | Advanced Complexity for Design                                                                                        |
| demo     | Demo mode will only return predefined results for debug and APIs purposes, for production, please use other settings. |

#### Requests Input Example

#### 


```curl
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
  -H "Content-Type: application/json" \
  -H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
  -d '{
    "unique_id": "craftsman-agent/craftsman-agent",
    "api_id": "jewelry_generator_hand_drawn_sketch",
    "data": {
      "prompt": "Rudy ring design with Oval Cut",
      "images": [],
      "template_id": "ring",
      "provider_model_id": "default",
      "options": {},
      "session_name": "Ruby Ring Design Oval Cut",
      "tag_list": "",
      "mode": "demo"
    }
  }'
```

#### Output Keys Definition
| Key                  | Description                                                             |
|----------------------|-------------------------------------------------------------------------|
| success              | Whether the design draft generation succeeded                           |
| share_url            | The URL of workspace containing the canvas to view the design           |
| blueprint            | Jewelry design blueprint data, when available                               |
| reference_images     | Generated reference image URLs                                          |
| final_image_url      | URL of the generated multi-view design sheet                            |
| options              | The options AI designer generated to display on the base jewelry models |
| session_id           | Workspace/session identifier                                            |
| title                | Generated session title                                                 |
| workspace_session_id | Workspace session identifier                                            |
| tag_list             | Tags associated with the generation                                     |


#### Output Example

The final hand drawn Style Images can be found in field: final_image_url

https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/d426ff6f-bd56-49d1-9ec9-54906bcc78bd.png

```commandline
{"success":true,"blueprint":{},"reference_images":["https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/d426ff6f-bd56-49d1-9ec9-54906bcc78bd.png"],"final_image_url":"https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/d426ff6f-bd56-49d1-9ec9-54906bcc78bd.png","overall_image":{},"session_id":"caef5381-ff26-4c7b-8c2f-d0da38f1c5c5","title":"Ruby Ring Design Oval Cut","workspace_session_id":"","tag_list":"","template_id":"ring","share_url":"https://craftsman-agent.aiagenta2z.com/app/sessions/share/caef5381-ff26-4c7b-8c2f-d0da38f1c5c5?pwd=0f38"}
```



### 2.2 CLI Usage

```shell
npx onekey agent craftsman-agent/craftsman-agent jewelry_generator_hand_drawn_sketch '{"prompt":"Rudy ring design with Oval Cut","images":[],"template_id":"ring","provider_model_id":"default","options":{},"session_name":"Ruby Ring Design Oval Cut","tag_list":"","mode":"demo"}'
```



