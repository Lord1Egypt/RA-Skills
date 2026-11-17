import QtQuick 2.12

// KPA Shelf v3 —— KONKR Pocket ADVANCE（960x640 / Android 12）
// 顶栏 | 左栏平台分类(按机种分组) | 中栏封面墙(3列) | 右栏游戏介绍
FocusScope {
    id: root
    focus: true

    property color colBg:     "#0d1016"
    property color colPanel:  "#161b24"
    property color colLine:   "#242c3a"
    property color colText:   "#ffffff"
    property color colDim:    "#8a94a8"
    property color colAccent: "#ff4d4d"

    // 重要：Pegasus 自带的 vpx() 在本机等于 v*0.75（按 853 高换算），
    // 所以用它写的 58/21/167 实际只渲染 43/15.7/125 —— 这正是"字和封面偏小"的根因。
    // 本主题不用 vpx，直接用 960×640 真实像素坐标。
    readonly property real kScale: 1.0
    function px(v) { return Math.round(v * kScale) }

    readonly property int columns: 4
    // 左栏宽度：v5 从 238 加宽到 252，给放大后的中文平台名留出空间
    readonly property int platW: 252

    property int  collIndex: 0
    property int  gridIndex: 0
    property bool inPlatforms: false

    property var  collObj: null
    property var  gamesModel: null
    property var  curGame: null
    property var  platModel: []

    // shortName -> { cn: 中文名, cat: 机种 }
    property var platMeta: ({
        "a2600":      { cn: "雅达利 2600",   cat: "家用机" },
        "dreamcast":  { cn: "世嘉 DC",       cat: "家用机" },
        "fc":         { cn: "任天堂 红白机",  cat: "家用机" },
        "md":         { cn: "世嘉 MD",       cat: "家用机" },
        "mdcd":       { cn: "世嘉 Mega-CD",  cat: "家用机" },
        "n64":        { cn: "任天堂 N64",    cat: "家用机" },
        "neogeo":     { cn: "SNK NEOGEO",    cat: "家用机" },
        "pce":        { cn: "PC Engine",     cat: "家用机" },
        "pcecd":      { cn: "PCE CD",        cat: "家用机" },
        "pico":       { cn: "世嘉 PICO",     cat: "家用机" },
        "ps":         { cn: "索尼 PS1",      cat: "家用机" },
        "saturn":     { cn: "世嘉 土星",     cat: "家用机" },
        "sega32x":    { cn: "世嘉 32X",      cat: "家用机" },
        "sfc":        { cn: "任天堂 超任",    cat: "家用机" },
        "sms":        { cn: "世嘉 SMS",      cat: "家用机" },

        "gb":         { cn: "任天堂 GB",     cat: "掌机" },
        "gba":        { cn: "任天堂 GBA",    cat: "掌机" },
        "gbc":        { cn: "任天堂 GBC",    cat: "掌机" },
        "gg":         { cn: "世嘉 GG",       cat: "掌机" },
        "nds":        { cn: "任天堂 NDS",    cat: "掌机" },
        "ngp":        { cn: "SNK NGP",       cat: "掌机" },
        "psp":        { cn: "索尼 PSP",      cat: "掌机" },
        "vb":         { cn: "任天堂 VB",     cat: "掌机" },
        "ws":         { cn: "万代 WS",       cat: "掌机" },

        "atomiswave": { cn: "ATOMISWAVE",    cat: "街机" },
        "cps1":       { cn: "CAPCOM CPS1",   cat: "街机" },
        "cps2":       { cn: "CAPCOM CPS2",   cat: "街机" },
        "cps3":       { cn: "CAPCOM CPS3",   cat: "街机" },
        "fbneo":      { cn: "FBNeo 全集合",   cat: "街机" },
        "mame":       { cn: "MAME 全集",     cat: "街机" },
        "naomi":      { cn: "世嘉 NAOMI",    cat: "街机" },
        "varcade":    { cn: "街机合集",      cat: "街机" },

        "dos":        { cn: "DOS 电脑",      cat: "电脑" },
        "msx":        { cn: "MSX 电脑",      cat: "电脑" },

        "android":    { cn: "安卓移植",      cat: "移植" },
        "easyrpg":    { cn: "RPG 制作大师",  cat: "移植" }
    })

    // ---------------- 焦点自愈 ----------------
    // 从游戏（RetroArch）返回后，Qt 窗口会重新激活，但根 FocusScope 不会自动拿回焦点，
    // 表现就是「界面完全正常，但所有按键都失灵」。这里低频检查并抢回焦点。
    Timer {
        id: focusGuard
        interval: 800
        running: true
        repeat: true
        onTriggered: {
            if (!root.activeFocus && root.visible) root.forceActiveFocus()
        }
    }

    // ---------------- 数据层 ----------------
    function buildPlatModel() {
        var cats = ["家用机", "掌机", "街机", "电脑", "移植", "其他"]
        var byCat = {}
        for (var c = 0; c < api.collections.count; c++) {
            var col = api.collections.get(c)
            var sn = String(col.shortName || col.name).toLowerCase()
            var info = platMeta[sn] || { cn: col.name, cat: "其他" }
            if (!byCat[info.cat]) byCat[info.cat] = []
            byCat[info.cat].push({ idx: c, sn: col.shortName ? col.shortName.toUpperCase() : col.name, cn: info.cn, n: col.games.count })
        }
        var out = []
        for (var i = 0; i < cats.length; i++) {
            var arr = byCat[cats[i]]
            if (!arr || arr.length === 0) continue
            arr.sort(function (a, b) { return a.sn.toLowerCase() < b.sn.toLowerCase() ? -1 : 1 })
            out.push({ head: cats[i], idx: -1 })
            for (var j = 0; j < arr.length; j++) {
                out.push({ head: "", idx: arr[j].idx, sn: arr[j].sn, cn: arr[j].cn, n: arr[j].n })
            }
        }
        platModel = out
    }

    function posOfColl(idx) {
        for (var i = 0; i < platModel.length; i++)
            if (platModel[i].idx === idx) return i
        return 0
    }

    // v5：L1/R1 直接切上/下一个平台，不用每次都按 ← 回左栏滚动
    function stepPlatform(dir) {
        var p = posOfColl(collIndex)
        var i = p + dir
        while (i >= 0 && i < platModel.length) {
            if (platModel[i].idx >= 0) { collIndex = platModel[i].idx; return }
            i += dir
        }
    }

    function refreshCollection() {
        if (api.collections.count === 0) {
            collObj = null; gamesModel = null; curGame = null; return
        }
        if (collIndex < 0) collIndex = 0
        if (collIndex >= api.collections.count) collIndex = api.collections.count - 1
        collObj = api.collections.get(collIndex)
        gamesModel = collObj ? collObj.games : null
        gridIndex = 0
        platList.positionViewAtIndex(posOfColl(collIndex), ListView.Contain)
        updateCur()
    }

    function updateCur() {
        if (!gamesModel || gamesModel.count === 0) { curGame = null; return }
        if (gridIndex < 0) gridIndex = 0
        if (gridIndex >= gamesModel.count) gridIndex = gamesModel.count - 1
        curGame = gamesModel.get(gridIndex)
    }

    function indexOfTitle(t) {
        if (!gamesModel) return -1
        for (var i = 0; i < gamesModel.count; i++) {
            var g = gamesModel.get(i)
            if (g && g.title === t) return i
        }
        return -1
    }

    function collectionOfTitle(t) {
        for (var c = 0; c < api.collections.count; c++) {
            var gm = api.collections.get(c).games
            for (var i = 0; i < gm.count; i++) {
                var g = gm.get(i)
                if (g && g.title === t) return c
            }
        }
        return -1
    }

    function launchCur() {
        if (!curGame) return
        api.memory.set('Shelf Game', curGame.title)
        api.memory.set('Shelf Collection', collIndex)
        saveTimer.stop()
        console.log("[SHELF] launch: " + curGame.title + " @ coll " + collIndex)
        curGame.launch()
    }

    function metaLine() {
        if (!curGame) return ""
        var p = []
        if (platformCn() !== "") p.push(platformCn())
        if (curGame.releaseYear > 0) p.push(curGame.releaseYear + " 年")
        var dev = curGame.developer || curGame.publisher
        if (dev) p.push(dev)
        if (curGame.genre) p.push(curGame.genre)
        if (curGame.players > 1) p.push(curGame.players + " 人同玩")
        if (p.length === 0 && collObj) p.push(collObj.name)
        return p.join("   ·   ")
    }

    function descText() {
        if (!curGame) return ""
        var d = curGame.description || curGame.summary || ""
        if (d === "") d = "本作暂无资料，可直接按 A 开始游戏。"
        return d
    }

    function statText() {
        if (!curGame) return ""
        var p = []
        if (curGame.playCount > 0) p.push("已玩 " + curGame.playCount + " 次")
        if (curGame.rating > 0) p.push("评分 " + Math.round(curGame.rating * 100) + "%")
        return p.join("    ")
    }

    function fileName() {
        if (!curGame || !curGame.files || curGame.files.length === 0) return ""
        var f = curGame.files[0]
        if (!f) return ""
        if (f.name) return String(f.name)
        var p = String(f.path || "")
        var i = p.lastIndexOf('/')
        return i >= 0 ? p.substring(i + 1) : p
    }

    function platformCn() {
        if (!collObj) return ""
        var sn = String(collObj.shortName || "").toLowerCase()
        var info = platMeta[sn]
        return info ? info.cn : collObj.name
    }

    // ---------------- 恢复上次位置 ----------------
    Component.onCompleted: {
        buildPlatModel()
        refreshCollection()

        var li = api.memory.has('Shelf Collection') ? Number(api.memory.get('Shelf Collection')) : -1
        var lg = api.memory.has('Shelf Game') ? String(api.memory.get('Shelf Game')) : ''
        if (lg === '' && api.memory.has('Last Game')) lg = String(api.memory.get('Last Game'))
        if (li < 0 && api.memory.has('Last Collection')) li = Number(api.memory.get('Last Collection'))

        if (lg !== '') {
            var i = -1
            if (li >= 0 && li < api.collections.count) {
                collIndex = li
                refreshCollection()
                i = indexOfTitle(lg)
            }
            if (i < 0) {
                var c = collectionOfTitle(lg)
                if (c >= 0 && c !== collIndex) { collIndex = c; refreshCollection() }
                i = indexOfTitle(lg)
            }
            if (i >= 0) {
                gridIndex = i
                updateCur()
                scrollTimer.restart()
                lateTimer.restart()
            }
            console.log("[SHELF] resume coll=" + collIndex + " idx=" + i + " title=" + lg)
        } else {
            console.log("[SHELF] first run, coll=" + collIndex)
        }
    }

    onCollIndexChanged: refreshCollection()
    onGridIndexChanged: { updateCur(); scrollTimer.restart() }
    onCurGameChanged: saveTimer.restart()

    Timer {
        id: scrollTimer
        interval: 30; repeat: false
        onTriggered: {
            if (root.gridIndex >= 0 && grid.count > 0)
                grid.positionViewAtIndex(root.gridIndex, GridView.Contain)
            platList.positionViewAtIndex(root.posOfColl(root.collIndex), ListView.Contain)
        }
    }

    // 主题重新加载后 GridView 布局要一点时间，二次定位更稳
    Timer {
        id: lateTimer
        interval: 400; repeat: false
        onTriggered: {
            if (root.gridIndex >= 0 && grid.count > 0)
                grid.positionViewAtIndex(root.gridIndex, GridView.Contain)
            platList.positionViewAtIndex(root.posOfColl(root.collIndex), ListView.Contain)
        }
    }

    Timer {
        id: saveTimer
        interval: 900; repeat: false
        onTriggered: {
            if (!root.curGame) return
            api.memory.set('Shelf Game', root.curGame.title)
            api.memory.set('Shelf Collection', root.collIndex)
            console.log("[SHELF] saved: " + root.curGame.title + " @ " + root.collIndex)
        }
    }

    // ---------------- 按键 ----------------
    // 安全调用 api.keys：某些 Pegasus 版本缺函数时返回 false，不让异常中断整条按键链
    function kIs(name, ev, fallbackKey) {
        if (api.keys && typeof api.keys[name] === "function") {
            try { return api.keys[name](ev) } catch (e) { return ev.key === fallbackKey }
        }
        return ev.key === fallbackKey
    }

    // try/catch 兜底：即使某个分支抛异常，下一次按键依然能正常处理
    Keys.onPressed: {
        try { handleKey(event) } catch (e) { console.log("[SHELF] key error: " + e) }
    }

    function handleKey(event) {
        console.log("[KEY] " + event.key)
        var c = root.columns

        // 方向键放最前：先保证移动光标这条链路一定可用
        if (kIs("isUp", event, Qt.Key_Up)) {
            event.accepted = true
            if (root.inPlatforms) {
                var p = root.posOfColl(root.collIndex) - 1
                while (p > 0 && root.platModel[p] && root.platModel[p].head !== "") p -= 1
                if (root.platModel[p] && root.platModel[p].idx >= 0) root.collIndex = root.platModel[p].idx
            } else if (root.gridIndex - c >= 0) root.gridIndex -= c
            return
        }
        if (kIs("isDown", event, Qt.Key_Down)) {
            event.accepted = true
            if (root.inPlatforms) {
                var q = root.posOfColl(root.collIndex) + 1
                while (q < root.platModel.length - 1 && root.platModel[q] && root.platModel[q].head !== "") q += 1
                if (root.platModel[q] && root.platModel[q].idx >= 0) root.collIndex = root.platModel[q].idx
            } else if (root.gamesModel && root.gridIndex + c < root.gamesModel.count) root.gridIndex += c
            return
        }
        if (kIs("isLeft", event, Qt.Key_Left)) {
            event.accepted = true
            if (!root.inPlatforms) {
                if (root.gridIndex % c === 0) root.inPlatforms = true
                else root.gridIndex -= 1
            }
            return
        }
        if (kIs("isRight", event, Qt.Key_Right)) {
            event.accepted = true
            if (root.inPlatforms) root.inPlatforms = false
            else if (root.gamesModel && root.gridIndex + 1 < root.gamesModel.count) root.gridIndex += 1
            return
        }
        if (kIs("isAccept", event, Qt.Key_Return)) {
            event.accepted = true
            if (root.inPlatforms) root.inPlatforms = false
            else root.launchCur()
            return
        }
        if (kIs("isCancel", event, Qt.Key_Escape)) {
            event.accepted = true
            root.inPlatforms = true
            return
        }
        // 注意：Pegasus 的函数名是 isPrevPage，不是 isPreviousPage。
        // 写错时 api.keys 里查不到该方法，会退化到 ev.key === Qt.Key_PageUp，
        // 而手柄 L1 的键值是 1048580（GamepadKeyId::L1），永远不相等 → L1 静默失效。
        if (kIs("isPrevPage", event, Qt.Key_PageUp)) {
            event.accepted = true
            root.stepPlatform(-1)
            return
        }
        if (kIs("isNextPage", event, Qt.Key_PageDown)) {
            event.accepted = true
            root.stepPlatform(1)
            return
        }
    }

    // ---------------- 背景 ----------------
    Rectangle { anchors.fill: parent; color: root.colBg }

    // ---------------- 顶栏 ----------------
    Rectangle {
        id: topBar
        width: parent.width; height: px(58)
        color: "#080b10"
        Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: root.colLine }

        Rectangle {
            x: px(20); width: px(4); height: px(26); color: root.colAccent
            anchors.verticalCenter: parent.verticalCenter
        }
        Text {
            x: px(34); anchors.verticalCenter: parent.verticalCenter
            text: "KPA 游戏库"
            color: root.colText; font.pixelSize: px(27); font.bold: true
        }
        Text {
            x: px(230); anchors.verticalCenter: parent.verticalCenter
            text: api.collections.count + " 个平台 · " + api.allGames.count + " 个游戏"
            color: root.colDim; font.pixelSize: px(15)
        }
        Row {
            anchors.right: parent.right; anchors.rightMargin: px(22)
            anchors.verticalCenter: parent.verticalCenter
            spacing: px(16)
            Text {
                text: root.platformCn()
                color: root.colText; font.pixelSize: px(21); font.bold: true
            }
            Text {
                text: (root.gridIndex + 1) + " / " + (root.gamesModel ? root.gamesModel.count : 0)
                color: root.colDim; font.pixelSize: px(17)
            }
        }
    }

    // ---------------- 左栏：平台分类 ----------------
    Rectangle {
        id: platPane
        x: 0; y: px(58); width: px(root.platW); height: parent.height - px(58)
        color: "#0f131b"
        clip: true
        Rectangle { anchors.right: parent.right; width: 1; height: parent.height; color: root.colLine }

        Rectangle {
            anchors.top: parent.top; width: parent.width; height: px(16); z: 5
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#0f131b" }
                GradientStop { position: 1.0; color: "#000f131b" }
            }
        }
        Rectangle {
            anchors.bottom: parent.bottom; width: parent.width; height: px(20); z: 5
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#000f131b" }
                GradientStop { position: 1.0; color: "#0f131b" }
            }
        }

        ListView {
            id: platList
            x: 0; y: px(6)
            width: parent.width; height: parent.height - px(12)
            model: root.platModel
            clip: true
            focus: false
            delegate: Item {
                width: platList.width
                height: modelData.head !== "" ? px(26) : px(56)
                property bool isHead: modelData.head !== ""
                property bool sel: !isHead && modelData.idx === root.collIndex

                // 分组标题：短横线 + 中文分类名（v5 加大到 15px）
                Rectangle {
                    visible: isHead
                    x: px(16); width: px(14); height: 1
                    anchors.bottom: parent.bottom; anchors.bottomMargin: px(8)
                    color: "#39445a"
                }
                Text {
                    visible: isHead
                    x: px(36); anchors.bottom: parent.bottom; anchors.bottomMargin: px(2)
                    text: modelData.head
                    color: "#8b96ab"
                    font.pixelSize: px(15)
                    font.bold: true
                    font.letterSpacing: px(3)
                }

                Rectangle {
                    visible: !isHead
                    anchors.fill: parent
                    color: sel ? "#1f2a3a" : "transparent"
                }
                Rectangle {
                    visible: sel; width: px(5); height: parent.height; color: root.colAccent
                }
                Rectangle {
                    visible: sel && root.inPlatforms
                    anchors.fill: parent
                    color: "transparent"
                    border.color: root.colAccent
                    border.width: px(2)
                }
                // 主名：中文机种名，v5 从 21px 提到 24px
                Text {
                    visible: !isHead
                    x: px(18); y: px(5)
                    width: parent.width - px(66)
                    text: isHead ? "" : modelData.cn
                    color: sel ? "#ffffff" : "#e6ecf7"
                    font.pixelSize: px(23)
                    font.bold: true
                    elide: Text.ElideRight
                }
                Text {
                    visible: !isHead
                    anchors.right: parent.right; anchors.rightMargin: px(13)
                    y: px(7)
                    text: isHead ? "" : modelData.n
                    color: sel ? root.colAccent : "#6b7688"
                    font.pixelSize: px(17)
                    font.bold: sel
                }
                // 副行：英文短名，帮助认平台
                Text {
                    visible: !isHead
                    x: px(19); y: px(34)
                    width: parent.width - px(34)
                    text: isHead ? "" : modelData.sn
                    color: sel ? "#a9b6cc" : "#7b8699"
                    font.pixelSize: px(13)
                    elide: Text.ElideRight
                }
                MouseArea {
                    anchors.fill: parent
                    enabled: !isHead
                    onClicked: root.collIndex = modelData.idx
                }
            }
        }
    }

    // ---------------- 中栏：封面墙（全宽 4 列） ----------------
    Rectangle {
        id: gridPane
        x: px(root.platW); y: px(58)
        width: parent.width - px(root.platW)
        height: parent.height - px(58) - px(166)
        color: root.colBg

        GridView {
            id: grid
            x: px(6); y: px(6)
            width: parent.width - px(12); height: parent.height - px(12)
            cellWidth: Math.floor(width / 4)
            cellHeight: px(268)
            model: root.gamesModel ? root.gamesModel : []
            clip: true
            focus: false
            delegate: Item {
                width: grid.cellWidth; height: grid.cellHeight
                property var g: root.gamesModel ? root.gamesModel.get(index) : null
                property bool sel: index === root.gridIndex

                Rectangle {
                    id: card
                    x: px(5); y: px(4)
                    width: parent.width - px(10); height: px(222)
                    radius: px(6)
                    color: "#121722"
                    border.width: sel ? px(3) : px(1)
                    border.color: sel ? root.colAccent : root.colLine

                    Image {
                        anchors.fill: parent; anchors.margins: px(3)
                        source: g ? (g.assets.boxFront || g.assets.screenshots[0] || "") : ""
                        fillMode: Image.PreserveAspectCrop
                        asynchronous: true
                        cache: true
                        smooth: true
                    }
                }
                Text {
                    anchors.top: card.bottom; anchors.topMargin: px(6)
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: parent.width - px(12)
                    text: g ? g.title : ""
                    color: sel ? root.colText : root.colDim
                    font.pixelSize: px(15)
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    maximumLineCount: 2
                    elide: Text.ElideRight
                    lineHeight: 1.1
                }
            }
        }

        // 顶部渐隐
        Rectangle {
            anchors.top: parent.top; width: parent.width; height: px(20); z: 6
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#0d1016" }
                GradientStop { position: 1.0; color: "#000d1016" }
            }
        }

        // 底部渐隐：滚动时下一行不会像被硬切
        Rectangle {
            anchors.bottom: parent.bottom; width: parent.width; height: px(26); z: 6
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#000d1016" }
                GradientStop { position: 1.0; color: "#0d1016" }
            }
        }

        Text {
            anchors.centerIn: parent
            visible: root.gamesModel && root.gamesModel.count === 0
            text: "该平台没有游戏"
            color: root.colDim; font.pixelSize: px(18)
        }
    }

    // ---------------- 底部：游戏介绍 ----------------
    Rectangle {
        id: detailPane
        x: px(root.platW); y: parent.height - px(166)
        width: parent.width - px(root.platW); height: px(166)
        color: "#10141c"
        clip: true
        Rectangle { anchors.top: parent.top; width: parent.width; height: 1; color: root.colLine }

        Rectangle {
            id: thumb
            x: px(14); y: px(14)
            width: px(96); height: px(128)
            radius: px(5)
            color: "#121722"
            border.width: px(1); border.color: root.colLine
            Image {
                anchors.fill: parent; anchors.margins: px(2)
                source: root.curGame ? (root.curGame.assets.boxFront || root.curGame.assets.screenshots[0] || "") : ""
                fillMode: Image.PreserveAspectCrop
                asynchronous: true
                cache: true
                smooth: true
            }
        }

        Text {
            id: titleTxt
            x: px(126); y: px(8)
            width: px(418)
            text: root.curGame ? root.curGame.title : "—"
            color: root.colText
            font.pixelSize: px(25); font.bold: true
            elide: Text.ElideRight
        }
        Text {
            id: metaTxt
            x: px(126); y: px(41)
            width: px(418)
            text: root.metaLine()
            color: root.colAccent
            font.pixelSize: px(14)
            elide: Text.ElideRight
        }
        Text {
            id: descTxt
            x: px(126); y: px(63)
            width: px(418)
            text: root.descText()
            color: "#c8d0dd"
            font.pixelSize: px(15)
            lineHeightMode: Text.FixedHeight
            lineHeight: px(23)
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            maximumLineCount: 3
            elide: Text.ElideRight
        }

        Text {
            anchors.right: parent.right; anchors.rightMargin: px(18)
            y: px(16)
            text: root.statText()
            color: root.colDim
            font.pixelSize: px(13)
        }
        Column {
            anchors.right: parent.right; anchors.rightMargin: px(18)
            y: px(44)
            spacing: px(7)
            Text { text: "A  开始游戏"; color: root.colAccent; font.pixelSize: px(14); font.bold: true }
            Text { text: "B  回平台栏"; color: root.colDim; font.pixelSize: px(13) }
            Text { text: "L1/R1  换平台"; color: root.colDim; font.pixelSize: px(13) }
            Text { text: "↑↓←→  选游戏"; color: root.colDim; font.pixelSize: px(13) }
        }
    }
}
