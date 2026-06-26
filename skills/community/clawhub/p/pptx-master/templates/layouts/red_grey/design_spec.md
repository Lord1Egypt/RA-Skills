# red grey - Design Specification v1.5

> This specification document defines the design principles, visual elements, layout structure, and technical specifications for the "red grey" PPT Template. It aims to ensure that all presentations created based on this template maintain a high degree of visual unity, professionalism, and aesthetics.

---

## I. Template Overview

| Property           | Description                                                                                                                                                                                                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Template Name**  | red grey                                                                                                                                                                                                                                                                                 |
| **Design Concept** | With "professionalism, rigor, and clarity" as the core, the design highlights the professionalism and authority of academic content through a minimalist design language and strong visual guidance. Red, as the primary color, symbolizes passion, rigor, and the spirit of innovation. |
| **Use Cases**      | Formal academic communication occasions such as academic reports, graduation defenses, thesis presentations, academic conference reports, and research result releases.                                                                                                                  |
| **Design Tone**    | Modern minimalist, professional and rigorous, strong academic feel, clear and readable.                                                                                                                                                                                                  |
| **Theme Mode**     | Light theme (light gray background with academic red accents), providing a unified and professional visual foundation.                                                                                                                                                                   |

---

## II. Canvas Specification

| Property         | Value                              | Notes                                                                                                                              |
| ---------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Format**       | Standard 16:9 widescreen           | Adapts to mainstream display devices for the best visual experience.                                                               |
| **Dimensions**   | 1280 × 720 px                      | Standard high-definition resolution to ensure content clarity.                                                                     |
| **viewBox**      | `0 0 1280 720`                     | Standard viewbox for SVG rendering to ensure accurate element positioning.                                                         |
| **Safe Margins** | Left/Right: 80px, Top/Bottom: 60px | Content should be placed within this area to avoid cropping or occlusion.                                                          |
| **Safe Area**    | x: 80-1200, y: 60-660              | Recommended placement area for core content.                                                                                       |
| **Grid Base**    | 20px                               | The spacing and dimensions of all layout elements should follow this base as much as possible to ensure alignment and consistency. |

---

## III. Color Scheme

### Core Colors

| Role             | Color Value | Notes                                                                                                                                                                                          |
| ---------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Academic Red** | `#D9001B`   | **Primary Color**. Used for the top-left decorative bar, title emphasis, key data, chart highlights, and brand identity, conveying rigor and vitality.                                         |
| **Deep Gray**    | `#333333`   | **Primary Text Color**. Used for page headings, chapter titles, body text headings, and other text that needs to be highlighted, ensuring optimal readability.                                 |
| **Medium Gray**  | `#666666`   | **Secondary Text Color**. Used for subtitles, body content, chart annotations, and other secondary information, creating a sense of hierarchy with Deep Gray.                                  |
| **Light Gray**   | `#F5F5F5`   | **Background Dominant Color**. Serves as the main background of the page, creating a clean, professional, and non-distracting visual foundation.                                               |
| **Pure White**   | `#FFFFFF`   | **Content Container Color**. Used for cards, chart backgrounds, highlight areas, etc., contrasting with the light gray background to突出内容.                                                      |
| **Footer Gray**  | `#E0E0E0`   | **Footer Background Color**. Used for the information bar at the bottom of the page, distinguishing it from the main background and increasing the structural sense and stability of the page. |

### Color Application Example

![Color Palette](https://via.placeholder.com/400x100/FFFFFF/FFFFFF?text=Color%20Palette:%20%23D9001B%20%23333333%20%23666666%20%23F5F5F5%20%23FFFFFF%20%23E0E0E0)
---

## IV. Typography System

### Font Stack

**Preferred Font**: `"思源黑体", "Source Han Sans", sans-serif`
**Compatible Font Stack**: `"思源黑体", "Arial", "Helvetica", sans-serif`

> **Design Note**: Source Han Sans is a modern, clear sans-serif font that supports multiple languages and is ideal for on-screen reading. Arial, as a cross-platform universal font, ensures good display results even in environments where Source Han Sans is not installed.

### Font Size Hierarchy

| Level   | Usage                                      | Desktop Size | Weight  | Color     |
| ------- | ------------------------------------------ | ------------ | ------- | --------- |
| H1      | Cover main title / End page title          | 48px         | Bold    | `#333333` |
| H2      | Page main title / Chapter page title       | 32px         | Bold    | `#333333` |
| H3      | TOC item title / Content area subtitle     | 22px         | Bold    | `#333333` |
| P       | Body content                               | 18px         | Regular | `#666666` |
| Caption | Auxiliary notes, chart labels, data source | 14px         | Regular | `#888888` |
| Footer  | Footer text                                | 14px         | Regular | `#666666` |

---

## V. Page Structure

### Common Layout Structure

| Area        | Position/Dimensions        | Description                                                                                                  |
| ----------- | -------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Header**  | y: 0-80px                  | Contains the top-left red decorative bar and an optional Logo area.                                          |
| **Title**   | y: 80-120px                | The page's main title area, located to the right of the top-left red decorative bar.                         |
| **Content** | y: 120-680px               | The main content display area with flexible layouts to accommodate text, images, charts, and other elements. |
| **Footer**  | y: 680-720px, Height: 40px | The bottom gray information bar containing copyright information, page numbers, logos, etc.                  |

### Spacing Guidelines

| Property                | Value | Description                                                |
| ----------------------- | ----- | ---------------------------------------------------------- |
| **Title Bottom Margin** | 24px  | Spacing between the title and the content below.           |
| **Module Gap**          | 40px  | Spacing between different content modules.                 |
| **Card Padding**        | 20px  | Distance between the content inside a card and its border. |
| **List Item Spacing**   | 16px  | Vertical spacing between each item in a list.              |

---

## VI. Core Design DNA

1. **Top-left Red Vertical Bar**: Located at the very top-left corner of the page, flush with the edge, with a width of 5px and a height of 50px. It serves as the visual starting point and brand identifier for the entire template, guiding the eye and emphasizing the title.
2. **Bottom Gray Bar**: Runs across the entire bottom of the page with a height of 40px. It stabilizes the page's visual center of gravity and provides a unified placement area for meta-information such as copyright and logos.
3. **Red Block Emphasis**: In scenarios like the table of contents page, a red background block is used to highlight the serial number, creating a strong visual contrast and guiding the audience to quickly understand the content structure.
4. **Rounded Rectangle**: On the cover and end pages, a red rounded rectangle is used to enclose the presenter information, adding a sense of design sophistication and approachability.

---

## VII. Page Types

### 1. Cover Page (01_cover.svg)

- **Layout**: Centered symmetrical layout.
- **Elements**:
  - Centered Logo at the top.
  - Centered main title and subtitle in the middle.
  - Centered red rounded rectangle at the bottom, containing presenter information.
  - Bottom gray footer.
- **Special**: **No** top-left red vertical bar to maintain the cover's simplicity and solemnity.
  
  ### 2. Table of Contents (02_toc.svg)
- **Layout**: Left-aligned title with a vertical list below.
- **Elements**:
  - Top-left red vertical bar.
  - Title "CONTENTS" to the right of the red bar.
  - Four vertically arranged TOC item cards below, each containing a red-background serial number and title.
  - Bottom gray footer.
    
    ### 3. Chapter Page (03_chapter.svg)
- **Layout**: Left-side visual focus with right-side white space.
- **Elements**:
  - Top-left red vertical bar.
  - A large chapter number and title to the right of the red bar, creating a strong visual impact.
  - Bottom gray footer.
    
    ### 4. Content Page (04_content.svg)
- **Layout**: Classic left-image, right-text layout.
- **Elements**:
  - Top-left red vertical bar.
  - Page title to the right of the red bar.
  - Image placeholder area on the left.
  - Text content area on the right, containing a subtitle and body text.
  - Bottom gray footer.
    
    ### 5. Ending Page (05_ending.svg)
- **Layout**: Centered symmetrical layout, echoing the cover page.
- **Elements**:
  - Centered Logo at the top.
  - Top-left red vertical bar.
  - Thank-you message to the right of the red bar.
  - Centered red rounded rectangle at the bottom, containing presenter information.
  - Bottom gray footer.

---

## VIII. Placeholder Specification

| Placeholder            | Description                                                      | Example                                               |
| ---------------------- | ---------------------------------------------------------------- | ----------------------------------------------------- |
| `{{LOGO}}`             | Placeholder for institutional or personal logo text or graphics. | "Huawei Technologies Co., Ltd." or Logo graphic       |
| `{{TITLE}}`            | Main title of the cover or chapter.                              | "Academic Report and Defense"                         |
| `{{SUBTITLE}}`         | Subtitle of the cover or report theme.                           | "A Study on Image Recognition Based on Deep Learning" |
| `{{AUTHOR}}`           | Presenter or author information.                                 | "Presenter: Zhang San"                                |
| `{{CHAPTER_NUM}}`      | Chapter number.                                                  | "01", "02"                                            |
| `{{CHAPTER_TITLE}}`    | Chapter title.                                                   | "Research Background and Significance"                |
| `{{THANK_YOU}}`        | Thank-you message on the ending page.                            | "Thank You for Listening"                             |
| `{{TOC_ITEM_N_TITLE}}` | TOC item title, where N is a number.                             | "Research Methodology", "Experimental Results"        |
| `{{COPYRIGHT}}`        | Copyright statement information.                                 | "© 2024 All Rights Reserved"                          |
| `{{PAGE_TITLE}}`       | Page title of a content page.                                    | "Experimental Design and Procedure"                   |
| `{{CONTENT_TITLE}}`    | Subtitle within the content area.                                | "Key Technical Points"                                |
| `{{CONTENT_BODY}}`     | Body paragraph in the content area.                              | "This study used the ... method for experiments..."   |

---

## IX. Usage Notes

1. **Logo Usage**: The logo should be placed in the designated placeholder position to ensure it is clearly visible and does not conflict with other elements.
2. **Color Extension**: If additional colors are needed, they should be selected from the adjacent colors or low-saturation colors of the primary color `#D9001B` to maintain the harmony and unity of the overall color scheme.
3. **Content Adaptation**: The template provides flexible layouts, but care should be taken with information density when filling content to avoid overcrowding.
4. **Font Consistency**: Try to install Source Han Sans on all devices to ensure the best visual.
5. **Brand Compliance**: If used for a specific organization, ensure all design elements and content comply with that organization's brand guidelines.
