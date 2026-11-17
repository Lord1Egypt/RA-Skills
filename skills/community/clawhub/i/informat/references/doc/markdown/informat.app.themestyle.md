<!-- DOCKEY: tst-9e4a0 -->
This document is the Informat application theme style documentation.

# Theme Style

## Overview

In certain specific situations, the preset styles of the Informat platform may not meet actual requirements and need to be adjusted. To solve this problem, the Informat platform provides an option for designers to write CSS styles. Designers can write CSS styles within the application designer to adjust and override default styles. The platform provides both **Application Theme** and **Module Theme** configuration capabilities to implement a modular concept, thereby improving loading and rendering efficiency when accessing modules.

## Prerequisites

When using theme styles to customize the appearance of your application, designers need to understand `CSS` related concepts. For those unfamiliar with frontend development, you can learn more by studying **CSS: Cascading Style Sheets**.


## Platform Implementation

The platform application designer supports independent CSS style configuration for both applications and modules. Theme styles are `automatically mounted` when **users enter an application or module**, and `automatically unmounted` when **users leave an application or module**.

The platform has standardized CSS **class** names for elements. We can override the application's **class** to achieve personalized display. Considering that the underlying platform version upgrades may change existing **class** names, the platform has also added styles prefixed with `theme-` on top of the corresponding **class** names. These styles will not change during platform upgrades, ensuring style compatibility.

## Customizing Dialog Styles with Theme Styles
The following example uses CSS styles to modify the system's default dialog style, adding a border and title text background color.
```css
.el-dialog{
    border: 2px solid #666 !important;
}
.informat-dialog-title{
    position: relative;
}
.informat-dialog-title::after{
    content: '';
    position: absolute;
    bottom: 0px;
    left: 0;
    background: rgb(141 244 157 / 50%);
    border-radius: 5px;
    width: 30px;
    height: 10px;
}
```

![Theme Style Dialog](./images/app-theme-dialog.png)

## Customizing Data Table Module Styles with Theme Styles
```css
/* Condition selector style override */
.app-module-Table.app-module-x1744czcz3blh .filter-item-op-condition-label {
    background: rgb(99,163,228);
    color: #fff;
}

/* Top toolbar */
.app-module-Table.app-module-x1744czcz3blh .table-module-toolbar {
    background: linear-gradient(90deg, transparent, rgb(225, 243, 216), transparent);
}

/* Filter conditions */
.app-module-Table.app-module-x1744czcz3blh .table-side-view .el-input__inner,
.app-module-Table.app-module-x1744czcz3blh .table-side-view .simple-select {
    background: #fff;
    border: 1px solid #ddd;
}

.info-view-box .form-opt-box, .record-opt-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    top: auto;
}
```