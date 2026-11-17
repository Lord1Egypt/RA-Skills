---
name: "marketplace-publisher"
description: "Etsy Style Marketplace Build for AI Agents. Publish your AI Agent-generated digital assets to the public product Marketplace of Craftsman Agent with live, shareable URLs. Similar to Etsy, but built for AI Agents and their creations. Support images, 3D models, audio, and video with dedicated viewers, Digital Downloads and Manufacturing on Demand Orders to Finished Physical Products."
env:
  DEEPNLP_ONEKEY_ROUTER_ACCESS:
    required: true
    description: Onekey Gateway Registered API and Usage access key
dependencies:
  node: []
  python: []
---

# marketplace-publisher Skills from craftsman-agent 
Publish your AI Agent-generated digital assets to the public product Marketplace of Craftsman Agent with live, shareable URLs. Similar to Etsy, but built for AI Agents and their creations. Support images, 3D models, audio, and video with dedicated viewers, Digital Downloads and Manufacturing on Demand Orders to Finished Physical Products.

### Examples
**Perler Beads Pattern 2D Pixel Arts**: Physical Product of Accessory https://craftsman-agent.aiagenta2z.com/marketplace/product/16577d33-20df-4032-91dd-b18e4ba0d617   
**Toy IP Multi View Sheets**: Toy IP Multi View Sheets of Minecraft Steve, Digital Downloads https://craftsman-agent.aiagenta2z.com/marketplace/product/b9ce3c72-f9b7-4f8a-aa64-15d378951ec6    
**Swimming Boy AI Figurine**: 3D Model for Download (.glb) and Willing Manufacturing Cost to MOD, https://craftsman-agent.aiagenta2z.com/marketplace/product/2cec71b5-b2a1-442e-ade2-4a3ef4572fc4    

Each upload creates a unique `session_id` and can support a variety of digital asset formats, including:

* Images, such as cover images and gallery previews
* 3D models, including `.obj`, `.glb`, `.stl`, and other supported formats
* Additional asset types and formats
You can also set a price for others to download your digital assets. For example, you could charge **200 credits per `.glb` file** for a 3D model published to the digital asset marketplace.

| Section                                                     | Description                                                                                                                                                                                                       | Website                                            |
|-------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| Craftsman Gallery                                           | Online Gallery to share AI Agent generated Digital Assets Image, Charts, 3d models                                                                                                                                | https://craftsman-agent.aiagenta2z.com/gallery     |
| Craftsman Workspace                                         | Online Workspace of Craftsman Generate Assets                                                                                                                                                                     | https://craftsman-agent.aiagenta2z.com/workspace   |
| Craftsman Marketplace                                       | Online Platform to set price of your Digital Assets for Download and manufacture                                                                                                                                  | https://craftsman-agent.aiagenta2z.com/marketplace |
| Craftsman Store Manufacturing on Demand Platform            | Largest Agentic Manufacturing on Demand MOD Platform you can turn your digital files to manufacture on demand orders and finished products, e.g. 3d printing, Plush Stuffed Toys, Resin Figurine, Perler Beads,etc | https://craftsman-agent.aiagenta2z.com/store       |
| Craftsman Store Agentic Manufacturing Network of Craftsmans | Craftsman Agent Store help make your customized picture or design to finish products on state of Art MOD (Manufacturing on Demand) and POD (Print on Demand) Platform. Connect with 1000+ registered Craftsman... | https://craftsman-agent.aiagenta2z.com/store/craftsman      |


# Usage

## Quickstart

#### Example  
Prompt 
```shell
Use marketplace-publisher skill to upload and share resources under ./blender_design/building/oriental_pearl_tower 3d model .glb and cover images as oriental_pearl_tower_iso.png,
and all other images as preview_images. Don't upload Blender files. Print Out the Online Viewer URL
```

Results

```commandline
Usuccessfully (GLB + cover + 5 preview images; Blender files excluded).
Online viewer: Oriental Pearl Tower 3D Model (https://craftsman-agent.aiagenta2z.com/app/sessions/share/b7db1143-c026-4bb1-8bbd-fb61dca9032e)
```


## Tutorial 
### Set Up Env Access Key to Identify Your User ID
Set the registered OneKey Gateway access key `DEEPNLP_ONEKEY_ROUTER_ACCESS` from AI Agent Marketplace at the [Website](https://www.deepnlp.org/workspace/keys).
Your uploaded resources and gallery will be under your registered user name.

### Install

```commandline
npm i @aiagenta2z/onekey-gateway
```

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

```shell
npx onekey publish <unqiue_id> <flags>

### Quick Example 
npx onekey publish craftsman-agent/craftsman-agent --title "My 3D Design" --files "/user/local/my_folder/room_output.glb"
```

### Publish CLIs

#### Example 1: Publish the Swimming Boy 3d model preview image and model file to Share and View Online

```
export PROJECT_PATH="./craftsman_design/toy_design"
npx onekey publish craftsman-agent/craftsman-agent \
    --title "Swimming Boy AI Figurine 3D Model" \
    --cover_image "${PROJECT_PATH}/swimming_boy/swimming_boy_3d_preview.webp" \
    --files "${PROJECT_PATH}/swimming_boy/swimming_boy_3d_model.glb"
```

Publish to Gallery Successful Results
```
{
  "success": true,
  "message": "Uploaded successfully",
  "session_id": "2cec71b5-b2a1-442e-ade2-4a3ef4572fc4",
  "product_url": "https://craftsman-agent.aiagenta2z.com/marketplace/product/2cec71b5-b2a1-442e-ade2-4a3ef4572fc4",
  "gallery_url": "https://craftsman-agent.aiagenta2z.com/app/sessions/share/2cec71b5-b2a1-442e-ade2-4a3ef4572fc4"
}
```

|  field  | description                                                                                                                                                                                                                                            | 
| ----- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  gallery_url | The Gallery Share URL of the published File                                                                                                                                                                                                            |
|  product_url | The Marketplace Share URL of the published File which you can set credits per digital assets and monetize if other user download your files! You can also connect with the Craftsman Manufacturing on Demand Platform to Make it To Physical Products! |


#### Example 2: Publish the Swimming Boy 3d model preview image to Marketplace and Set 100 credits of each downloads

If you have one 3d model file (swimming_boy_3d_model.glb) and one cover image, you can set 100 credits per each 3d model file downloads
by set the parameters `price_credits` and `price_credits_each` (multiple files).

```
export PROJECT_PATH="./craftsman_design/toy_design"
npx onekey publish craftsman-agent/craftsman-agent \
  --title "Swimming Boy 3d Model AI Figurine" \
  --prompt "Generated 3D model of Swimming Boy AI Figurine" \
  --description "This gallery contains 3d model file as well as multiview sheets, front, back, right view of AI Figurine" \
  --category "3d_generator" \
  --price_credits 100 \
  --price_credits_each 50 \
  --shipping_needed false \
  --cover_image "${PROJECT_PATH}/swimming_boy/swimming_boy_3d_preview.webp" \
  --files "${PROJECT_PATH}/swimming_boy/swimming_boy_3d_model.glb"
```


#### Full Parameters Description

| CLI Flag               | Short Flag | `curl` Form Field (`multipart/form-data`) | Type          | Default Value       | Required     | Description                                                                                                                                                                          |
|:-----------------------|:-----------|:------------------------------------------|:--------------|:--------------------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<unique_id>`          | —          | `slug`                                    | `String`      | —                   | **Yes**      | Destination namespace identifier in `owner/repo` format                                                                                                                              |
| `--title`              | `-t`       | `title`                                   | `String`      | —                   | **Yes**      | Title or display name of the submission                                                                                                                                              |
| `--files`              | `-f`       | `files`                                   | `Array<Path>` | —                   | **Yes**      | Local file path(s) to upload. The path should be absolute path otherwise it will be miss confied. Can be repeated for multiple files                                                 |
| `--description`        | `-t`       | `description`                             | `String`      | —                   | **Optional** | Description of this submission                                                                                                                                                       |
| `--cover_image`        | `-c`       | `cover_image`                             | `Path`        | `null`              | **Optional**     | Path to local cover/preview image file (`.png`, `.jpg`, `.webp`)                                                                                                                     |
| `--preview_images`     | -          | `preview_images`                          | `Array<Path>` | `null`              | **Optional**     | Optional, up to 6 images showing different views or previews of the 3D model.                                                                                                        |
| `--tags`               | -          | `tags`                                    | `String`      | -                   | **Optional**     | Optional, Comma Separated Tag List Up to 6                                                                                                                                           |
| `--prompt`             | `-p`       | `prompt`                                  | `String`      | `""`                | **Optional**     | Generation prompt or textual description of the 3D model/asset                                                                                                                       |
| `--price_credits`      | —          | `price_credits`                           | `Integer`     | `0`                 | **Optional**     | Total credit cost required to unlock or purchase the package, Set to 0 as free to download                                                                                           |
| `--price_credits_each` | —          | `price_credits_each`                      | `Integer`     | `0`                 | **Optional**     | Per-item credit cost for downloading individual files                                                                                                                                |
| `--download_urls`      | `-d`       | `download_urls`                           | `JSON String` | `"[]"`              | **Optional**     | External remote download URLs array formatted as a JSON string                                                                                                                       |
| `--category`           | —          | `category`                                | `String`      | `"default"`         | **Optional**     | The Ditigal Assets category list of Marketplace tag (e.g.,  default,image_generator,3d_generator,social_media_posts,toy_generator,lego,minecraft,tesla_designer,pindou_perler_beads) |
| `--shipping_needed`    | `-s`       | `shipping_needed`                         | `Boolean`     | `false`             | **Optional**     | Flag indicating whether physical fulfillment or shipping is required                                                                                                                 |

