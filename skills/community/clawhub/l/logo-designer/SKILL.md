---
name: "logo-designer-generator"
description: "AI Logo Designer Skills to Generate Multi-Page Image Carousels from Templates of Logo Designers Sota Models Nano Banana, Nano Banana-2 ,Imagen-2 and more are available"
env:
  DEEPNLP_ONEKEY_ROUTER_ACCESS:
    required: true
    description: Onekey Gateway Registered API and Usage access key
dependencies:
  node: []
  python: []
---

# AI Logo Designer Skills from craftsman-agent

Auto-generated skill for OneKey Agent Gateway registered agent `craftsman-agent/craftsman-agent` for the `image_generator` API.

| Section                                          | Description                                                |
|--------------------------------------------------|------------------------------------------------------------|
| Craftsman Image Generator Console Online         | https://craftsman-agent.aiagenta2z.com/app/image-generator |
| Craftsman Website                                | https://craftsman-agent.aiagenta2z.com                     |
| Craftsman App                                    | https://craftsman-agent.aiagenta2z.com/app                 |
| Craftsman Gallery                                | https://craftsman-agent.aiagenta2z.com/gallery             |
| Craftsman Workspace                              | https://craftsman-agent.aiagenta2z.com/workspace           |
| Craftsman Marketplace                            | https://craftsman-agent.aiagenta2z.com/marketplace         |
| Craftsman Store Manufacturing on Demand Platform | https://craftsman-agent.aiagenta2z.com/store               |

## Quick Start
Set the registered OneKey Gateway access key `DEEPNLP_ONEKEY_ROUTER_ACCESS` from AI Agent Marketplace at the [Website](https://deepnlp.org/workspace/keys).

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

## 1. API Usage

Task: Generate an AI Post of topic `Introduction to Difference between MCPs,Skills and Agents CLIs`
Prompt: Introduction to Difference between MCPs,Skills and Agents CLIs

### OneKey Router

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "image_generator",
  "data": {
    "prompt": "Introduction to Difference between MCPs,Skills and Agents CLIs",
    "images": [],
    "card_count": 1,
    "template_id": "logo-designer",    
    "api_id": "image_generator",
    "asset_size": [
        {"width": 1080, "height": 1080, "ratio": "1:1"}
    ],
    "mode": "basic",
    "session_id": "31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb",
    "session_name": "AI Poster of MCPs/CLIs/Agents",
    "tag_list": "",
    "model": "default",
    "styles": [
      "Editorial grid layout with corporate dark deep monochromatic tones"
    ],
    "design_config": {"template_id":"logo-designer","card_count":1,"card_count_source":"default","channel_profile":"generic","audience_profile":"general","age_band":"auto","profile_version":"1.0.0","geometry_source":"profile","resolved_profiles":[{"type":"channel","id":"generic","version":"1.0.0"},{"type":"audience","id":"general","version":"1.0.0"}],"language":"auto","mode":"standard","text_model":"default","image_model":"default","styles":["Editorial grid layout with corporate dark deep monochromatic tones"],"constraints":["Limit target output build to 6 high-density pages max for physical double folding print"],"brief_inputs":[{"id":"binp-1","type":"prompt","content":"Introduction to Difference between MCPs,Skills and Agents CLIs"},{"id":"binp-2","type":"style","content":"Editorial grid layout with corporate dark deep monochromatic tones"},{"id":"binp-3","type":"constraint","content":"Limit target output build to 6 high-density pages max for physical double folding print"},{"id":"binp-1786857754660","type":"prompt","content":"Custom newly configured prompt parameter specifications instructions layout metric..."}],"text_styles":{"brand":{"color":"#8b5cf6","font":"Playfair Display","font_size":"20px","font_weight":"600","text_align":"left","line_height":1.3,"letter_spacing":0},"headline":{"color":"#8b5cf6","font":"Playfair Display","font_size":"18px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0},"content":{"color":"#8b5cf6","font":"Playfair Display","font_size":"16px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0},"footer":{"color":"#8b5cf6","font":"Playfair Display","font_size":"16px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0}},"page_templates":[{"id":"image-generator-01","label":"Cover Page","layers":[{"id":"l-bg","type":"background","name":"Backdrop","position":{"x":0,"y":0},"size":{"width":1080,"height":1350},"style_overrides":[],"if_selected":false},{"id":"l-brand","type":"brand","name":"Your Brand","position":{"x":40,"y":40},"size":{"width":200,"height":40},"style_overrides":[],"if_selected":false},{"id":"l-img","type":"image","name":"Graphic URL","position":{"x":150,"y":180},"size":{"width":780,"height":700},"style_overrides":[],"if_selected":false},{"id":"l-headline","type":"text","name":"Headline","position":{"x":40,"y":850},"size":{"width":400,"height":80},"style_overrides":[],"if_selected":false},{"id":"l-content","type":"text","name":"Content","position":{"x":40,"y":950},"size":{"width":400,"height":80},"style_overrides":[],"if_selected":false},{"id":"l-cta","type":"cta","name":"Footer","position":{"x":0,"y":1150},"size":{"width":1080,"height":50},"style_overrides":[],"if_selected":false}]}]}
  }
}'
```

### Request Parameters

| Field         | Required | Description                                                                                                                            |
|---------------|----------|----------------------------------------------------------------------------------------------------------------------------------------|
| prompt        | Required | Text, User Input Design Goal, e.g. `Genreate a movie character description of Movie Odyssey`                                             |
| images        | Required | List of Reference Images that user uploads                                                                                             |
| onekey        | Required | DeepNLP Router OneKey Program                                                                                                          |
| api_id        | Required | user `image_generator` to represent image generator                                                                                    | 
| template_id   | Required | e.g.    logo-designer,social-media-carousel,presentation,app-store,logo-designer,logo-designer,photo-editor                                |
| card_count    | Required | int, e.g. 4 cards of instagram/twitter/xiaohongshu                        | 
| asset_size    | Required | List of Asset Size Available, default to templates, such as List of width,height,ratio, {"width": 1080, "height": 1080, "ratio": "1:1"} |
| mode          | Optional | The design complexity, basic,standard,advanced                                                                                         |
| styles        | Optional | List, List of Styles Prompt, e.g. deep monochromatic tones,techonology styles                                                          |
| design_config | Optional | Dict, Detailed Layers of Text, Prompt, Images on the Slides                                                                            |

### Design Config Layers AI Brief

| Field       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| template_id | Template ID, supported values: logo-designer,social-media-carousel,presentation,app-store,logo-designer,logo-designer,photo-editor                                                                                                                                                                                                                                                                                                                                                                                                                    |
| card_count  | 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| asset_size  | 1:1,4:5,9:16,A4 (7:10),A3 (7:10),A2 (7:10)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ratio       | 1:1,4:5,9:16,A4 (7:10),A3 (7:10),A2 (7:10)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| width       | 1080                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| height      | 1080                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| geometry    | widthxheight                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| styles      | List of Styles Blocks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| constraints | List of Constraints Blocks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| brief_inputs       | List of Design Layers, such as `[{"id":"binp-1","type":"prompt","content":"Introduction to Difference between MCPs,Skills and Agents CLIs"},{"id":"binp-2","type":"style","content":"Editorial grid layout with corporate dark deep monochromatic tones"},{"id":"binp-3","type":"constraint","content":"Limit target output build to 6 high-density pages max for physical double folding print"},{"id":"binp-1786857754660","type":"prompt","content":"Custom newly configured prompt parameter specifications instructions layout metric..."}]` |
| brief_inputs[i].id | {"id":"binp-1","type":"prompt","content":"Introduction to Difference between MCPs,Skills and Agents CLIs"}                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| brief_inputs[i].type | {"id":"binp-1","type":"prompt","content":"Introduction to Difference between MCPs,Skills and Agents CLIs"}                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| brief_inputs[i].content | {"id":"binp-1","type":"prompt","content":"Introduction to Difference between MCPs,Skills and Agents CLIs"}                                                                                                                                                                                                                                                                                                                                                                                                                                        |


### API Expected Outputs

### Results Parameters

| Field      | Description                                                                                                                        |
|------------|------------------------------------------------------------------------------------------------------------------------------------|
| session_id | The unique id of AI Generated Images/Slides/Carousels                                                                              |
| title      | The title of the genreate Slides                                                                                                   |
| share_url | The workspace of this generate slides, you can open workspace an edit the generated text,color,size and export the final images... |
| card_count                              | The Int value of Card Counts of Generated 4 Pages of Instagram/Twitter/Xiaohongshu Slides                                          |
| images                                  | List of url, The List of Main Generated Images from AI Image Generator, Each Card Have one image                                   |
| data                                    | The text/references images displayed as layers on the main images.                                                                 |
| data.sequence_pages                     | List of Design Generated Layers config: The text,headline,content                                                                  |
| data.sequence_pages[i]                  | Dict of Pages Data                                                                                                                 |
| data.sequence_pages[i].id               | The ID of the generated Pages                                                                                                      |
| data.sequence_pages[i].label              | The Label of the generated Pages                                                                                                   |
| data.sequence_pages[i].geometry           | The geometry of the generated Page, following the formats of "widthxheight"                                                        |
| data.sequence_pages[i].canvas_width       | The width of the generated Page, e.g. 1080                                                                                         |
| data.sequence_pages[i].canvas_height      | The height of the generated Page, e.g. 1350                                                                                        |
| data.sequence_pages[i].layers             | Layers config: List of Layers Data, text,headline,content displayed                                                                |
| data.sequence_pages[i].layers[j].id       | Int, Card ID                                                                                                                       |
| data.sequence_pages[i].layers[j].type     | String, Supported Type: background,text,image,headline                                                                             |
| data.sequence_pages[i].layers[j].position | Dict of {"x": 0,"y": 0}, position of the text layer display on the main canvas                                                     |
| data.sequence_pages[i].layers[j].position | Dict of x,y position of the text layer display on the main canvas                                                                  |

Note: To Export the Final Multi Slides Images, You can visit the share_url workspace and export the images to .pdf,.png,.ppt formats.

`share_url`: https://craftsman-agent.aiagenta2z.com/app/sessions/share/547083a4-5e38-4e4e-ba78-300cadb88b11

It will show a board of card count, e.g. 4 pages of ready to use knowledge cards of social media posts!

```json
{
  "success": true,
  "partial_success": false,
  "failed_card_indexes": [],
  "summary": "MCPs, Skills & Agents CLI Explained",
  "final_image_url": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/ed2a4a2a-50af-403b-831c-4e97194e2ec6.png",
  "images": [
    {
      "url": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/ed2a4a2a-50af-403b-831c-4e97194e2ec6.png"
    }
  ],
  "share_url": "https://craftsman-agent.aiagenta2z.com/app/sessions/share/31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb",
  "channel_profile": "generic",
  "audience_profile": "general",
  "age_band": "auto",
  "profile_version": "1.0.0",
  "geometry": "1080x1350",
  "geometry_source": "profile",
  "resolved_profiles": [
    {
      "type": "channel",
      "id": "generic",
      "version": "1.0.0"
    },
    {
      "type": "audience",
      "id": "general",
      "version": "1.0.0"
    }
  ],
  "data": {
    "schema_version": "image-generator.v1",
    "style_profile": {
      "channel": {
        "id": "generic",
        "version": "1.0.0"
      },
      "audience": {
        "id": "general",
        "version": "1.0.0"
      },
      "age_band": "auto",
      "profile_version": "1.0.0"
    },
    "geometry": "1080x1350",
    "geometry_source": "profile",
    "sequence_pages": [
      {
        "id": "card-01",
        "label": "CLI Concepts Overview",
        "geometry": "1080x1350",
        "canvas_width": 1080,
        "canvas_height": 1350,
        "generation": {
          "status": "success",
          "attempts": 1,
          "image_prompt": "clean editorial illustration. cohesive editorial illustration with generous negative space. Palette: #F7F3EA, #172033, #6D5DFB. Abstract editorial illustration showing three interconnected nodes labeled conceptually as protocol, function, and actor, using deep navy and violet tones on cream background, clean lines, no text, no letters, no typography, no watermark. No text, no letters, no typography, no watermark. Reserve clean negative space for editable title and body layers. Compose specifically for a 1:1 frame and keep every focal subject fully inside a centered safe area."
        },
        "content_blocks": [
          {
            "label": "MCPs",
            "content": "Protocols\nstandardizing model\ninteraction—think\nAPIs for AI\nreasoning."
          },
          {
            "label": "Skills",
            "content": "Self-contained\nfunctions (e.g.,\nsearch, math) that\nagents can invoke as\nneeded."
          },
          {
            "label": "Agents",
            "content": "Autonomous CLI\nprograms that chain\nMCPs and Skills to\ncomplete goals."
          }
        ],
        "layers": [
          {
            "id": "card-01-bg",
            "type": "background",
            "name": "Background",
            "value": "#F7F3EA",
            "position": {
              "x": 0,
              "y": 0
            },
            "size": {
              "width": 1080,
              "height": 1350
            },
            "if_selected": false,
            "style_overrides": []
          },
          {
            "id": "card-01-brand",
            "type": "brand",
            "name": "Brand",
            "value": "AI Dev Tools",
            "position": {
              "x": 40,
              "y": 40
            },
            "size": {
              "width": 200,
              "height": 40
            },
            "if_selected": false,
            "color": "#172033",
            "font": "Inter",
            "font_size": "20px",
            "font_weight": "600",
            "style_overrides": []
          },
          {
            "id": "card-01-headline",
            "type": "text",
            "name": "Headline",
            "value": "MCPs, Skills & Agents: What’s the Difference?",
            "position": {
              "x": 40,
              "y": 850
            },
            "size": {
              "width": 400,
              "height": 80
            },
            "if_selected": false,
            "color": "#172033",
            "font": "Inter",
            "font_size": "48px",
            "font_weight": "700",
            "style_overrides": []
          },
          {
            "id": "card-01-image",
            "type": "image",
            "name": "Illustration",
            "value": "https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/ed2a4a2a-50af-403b-831c-4e97194e2ec6.png",
            "position": {
              "x": 150,
              "y": 180
            },
            "size": {
              "width": 780,
              "height": 700
            },
            "color": "#000000",
            "image_fit": "contain",
            "if_selected": false,
            "style_overrides": []
          },
          {
            "id": "card-01-content-block-01",
            "type": "text",
            "name": "Content Block 01",
            "value": "MCPs\nProtocols\nstandardizing model\ninteraction—think\nAPIs for AI\nreasoning.",
            "position": {
              "x": 80,
              "y": 918
            },
            "size": {
              "width": 289,
              "height": 304
            },
            "if_selected": false,
            "color": "#172033",
            "font": "Inter",
            "font_size": "20px",
            "font_weight": "400",
            "line_height": 1.2
          },
          {
            "id": "card-01-content-block-02",
            "type": "text",
            "name": "Content Block 02",
            "value": "Skills\nSelf-contained\nfunctions (e.g.,\nsearch, math) that\nagents can invoke as\nneeded.",
            "position": {
              "x": 396,
              "y": 918
            },
            "size": {
              "width": 289,
              "height": 304
            },
            "if_selected": false,
            "color": "#172033",
            "font": "Inter",
            "font_size": "20px",
            "font_weight": "400",
            "line_height": 1.2
          },
          {
            "id": "card-01-content-block-03",
            "type": "text",
            "name": "Content Block 03",
            "value": "Agents\nAutonomous CLI\nprograms that chain\nMCPs and Skills to\ncomplete goals.",
            "position": {
              "x": 711,
              "y": 918
            },
            "size": {
              "width": 289,
              "height": 304
            },
            "if_selected": false,
            "color": "#172033",
            "font": "Inter",
            "font_size": "20px",
            "font_weight": "400",
            "line_height": 1.2
          },
          {
            "id": "card-01-footer",
            "type": "cta",
            "name": "Footer",
            "value": "Page 1 of 6 — Foundations of AI Command-Line Tools",
            "position": {
              "x": 0,
              "y": 1150
            },
            "size": {
              "width": 1080,
              "height": 50
            },
            "if_selected": false,
            "color": "#6D5DFB",
            "font": "Inter",
            "font_size": "16px",
            "font_weight": "400",
            "style_overrides": []
          }
        ]
      }
    ],
    "card_count": 1
  },
  "card_count": 1,
  "card_count_source": "default",
  "session_id": "31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb",
  "title": "Lego Build Plan",
  "workspace_session_id": "",
  "tag_list": "",
  "description": "Prompt: Introduction to Difference between MCPs,Skills and Agents CLIs, Styles: Editorial grid layout with corporate dark deep monochromatic tones, Constraints: Limit target output build to 6 high-density pages max for physical double folding print, Prompt: Custom newly configured prompt parameter specifications instructions layout metric..."
}
```

### Example Input Design Config
key: design_config
value: 

```json
{
      "template_id": "logo-designer",
      "card_count": 1,
      "card_count_source": "default",
      "channel_profile": "generic",
      "audience_profile": "general",
      "age_band": "auto",
      "profile_version": "1.0.0",
      "geometry_source": "profile",
      "resolved_profiles": [{
        "type": "channel",
        "id": "generic",
        "version": "1.0.0"
      }, {
        "type": "audience",
        "id": "general",
        "version": "1.0.0"
      }],
      "language": "auto",
      "mode": "standard",
      "text_model": "default",
      "image_model": "default",
      "styles": ["Editorial grid layout with corporate dark deep monochromatic tones"],
      "constraints": ["Limit target output build to 6 high-density pages max for physical double folding print"],
      "brief_inputs": [{
        "id": "binp-1",
        "type": "prompt",
        "content": "Introduction to Difference between MCPs,Skills and Agents CLIs"
      }, {
        "id": "binp-2",
        "type": "style",
        "content": "Editorial grid layout with corporate dark deep monochromatic tones"
      }, {
        "id": "binp-3",
        "type": "constraint",
        "content": "Limit target output build to 6 high-density pages max for physical double folding print"
      }, {
        "id": "binp-1786857754660",
        "type": "prompt",
        "content": "Custom newly configured prompt parameter specifications instructions layout metric..."
      }],
      "text_styles": {
        "brand": {
          "color": "#8b5cf6",
          "font": "Playfair Display",
          "font_size": "20px",
          "font_weight": "600",
          "text_align": "left",
          "line_height": 1.3,
          "letter_spacing": 0
        },
        "headline": {
          "color": "#8b5cf6",
          "font": "Playfair Display",
          "font_size": "18px",
          "font_weight": "400",
          "text_align": "left",
          "line_height": 1.3,
          "letter_spacing": 0
        },
        "content": {
          "color": "#8b5cf6",
          "font": "Playfair Display",
          "font_size": "16px",
          "font_weight": "400",
          "text_align": "left",
          "line_height": 1.3,
          "letter_spacing": 0
        },
        "footer": {
          "color": "#8b5cf6",
          "font": "Playfair Display",
          "font_size": "16px",
          "font_weight": "400",
          "text_align": "left",
          "line_height": 1.3,
          "letter_spacing": 0
        }
      },
      "page_templates": [{
        "id": "image-generator-01",
        "label": "Cover Page",
        "layers": [{
          "id": "l-bg",
          "type": "background",
          "name": "Backdrop",
          "position": {
            "x": 0,
            "y": 0
          },
          "size": {
            "width": 1080,
            "height": 1350
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-brand",
          "type": "brand",
          "name": "Your Brand",
          "position": {
            "x": 40,
            "y": 40
          },
          "size": {
            "width": 200,
            "height": 40
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-img",
          "type": "image",
          "name": "Graphic URL",
          "position": {
            "x": 150,
            "y": 180
          },
          "size": {
            "width": 780,
            "height": 700
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-headline",
          "type": "text",
          "name": "Headline",
          "position": {
            "x": 40,
            "y": 850
          },
          "size": {
            "width": 400,
            "height": 80
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-content",
          "type": "text",
          "name": "Content",
          "position": {
            "x": 40,
            "y": 950
          },
          "size": {
            "width": 400,
            "height": 80
          },
          "style_overrides": [],
          "if_selected": false
        }, {
          "id": "l-cta",
          "type": "cta",
          "name": "Footer",
          "position": {
            "x": 0,
            "y": 1150
          },
          "size": {
            "width": 1080,
            "height": 50
          },
          "style_overrides": [],
          "if_selected": false
        }]
      }]
    }
```

## 2. CLIs Usage

```bash

export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
npx onekey agent craftsman-agent/craftsman-agent image_generator '{"prompt":"Introduction to Difference between MCPs,Skills and Agents CLIs","images":[],"card_count":1,"template_id":"logo-designer","api_id":"image_generator","asset_size":[{"width":1080,"height":1080,"ratio":"1:1"}],"mode":"basic","session_id":"31d57eb9-9a37-4808-9c5b-1bfbb2abf5fb","session_name":"AI Poster of MCPs/CLIs/Agents","tag_list":"","model":"default","styles":["Editorial grid layout with corporate dark deep monochromatic tones"],"design_config":{"template_id":"logo-designer","card_count":1,"card_count_source":"default","channel_profile":"generic","audience_profile":"general","age_band":"auto","profile_version":"1.0.0","geometry_source":"profile","resolved_profiles":[{"type":"channel","id":"generic","version":"1.0.0"},{"type":"audience","id":"general","version":"1.0.0"}],"language":"auto","mode":"standard","text_model":"default","image_model":"default","styles":["Editorial grid layout with corporate dark deep monochromatic tones"],"constraints":["Limit target output build to 6 high-density pages max for physical double folding print"],"brief_inputs":[{"id":"binp-1","type":"prompt","content":"Introduction to Difference between MCPs,Skills and Agents CLIs"},{"id":"binp-2","type":"style","content":"Editorial grid layout with corporate dark deep monochromatic tones"},{"id":"binp-3","type":"constraint","content":"Limit target output build to 6 high-density pages max for physical double folding print"},{"id":"binp-1786857754660","type":"prompt","content":"Custom newly configured prompt parameter specifications instructions layout metric..."}],"text_styles":{"brand":{"color":"#8b5cf6","font":"Playfair Display","font_size":"20px","font_weight":"600","text_align":"left","line_height":1.3,"letter_spacing":0},"headline":{"color":"#8b5cf6","font":"Playfair Display","font_size":"18px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0},"content":{"color":"#8b5cf6","font":"Playfair Display","font_size":"16px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0},"footer":{"color":"#8b5cf6","font":"Playfair Display","font_size":"16px","font_weight":"400","text_align":"left","line_height":1.3,"letter_spacing":0}},"page_templates":[{"id":"image-generator-01","label":"Cover Page","layers":[{"id":"l-bg","type":"background","name":"Backdrop","position":{"x":0,"y":0},"size":{"width":1080,"height":1350},"style_overrides":[],"if_selected":false},{"id":"l-brand","type":"brand","name":"Your Brand","position":{"x":40,"y":40},"size":{"width":200,"height":40},"style_overrides":[],"if_selected":false},{"id":"l-img","type":"image","name":"Graphic URL","position":{"x":150,"y":180},"size":{"width":780,"height":700},"style_overrides":[],"if_selected":false},{"id":"l-headline","type":"text","name":"Headline","position":{"x":40,"y":850},"size":{"width":400,"height":80},"style_overrides":[],"if_selected":false},{"id":"l-content","type":"text","name":"Content","position":{"x":40,"y":950},"size":{"width":400,"height":80},"style_overrides":[],"if_selected":false},{"id":"l-cta","type":"cta","name":"Footer","position":{"x":0,"y":1150},"size":{"width":1080,"height":50},"style_overrides":[],"if_selected":false}]}]}}'

```

