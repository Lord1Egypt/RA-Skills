/**
 * 哈萨克语输入法 (OpenClaw Kazakh IME)
 * 版本: 1.3.0
 * 发布日期: 2026-04-06
 * 
 * 功能特性:
 * - 三种输入模式：英文模式、哈萨克语阿拉伯文模式、哈萨克语西里尔文模式
 * - 循环切换：按 Ctrl+Shift+K 循环切换三种输入模式
 * - 虚拟键盘：内置可拖动的虚拟键盘，支持触屏设备
 * - 字符映射：完整的英文键盘到哈萨克文字符的映射
 * - 组合键支持：支持 Ctrl+C、Ctrl+V 等系统快捷键
 * - 智能识别：自动适配输入元素，支持动态添加的输入框
 * 
 * 使用方法:
 * 1. 在 HTML 文件中引入此脚本
 * 2. 按 Ctrl+Shift+K 切换输入模式
 * 3. 使用英文键盘输入，字符会自动转换为对应模式的哈萨克文字符
 * 
 * 作者: OpenClaw Team
 * 许可证: 仅供学习和使用
 */

(function(){
    // 字体设置变量
    const FONT_SETTINGS = {
        // 阿拉伯文字体：支持哈萨克语阿拉伯文书写系统
        arabic: 'UKK TZK1, Microsoft Uighur, sans-serif',
        // 西里尔文字体：支持哈萨克语西里尔文书写系统
        cyrillic: 'UKK TZK1, sans-serif',
        // 英文字体：默认系统字体
        english: ''
    };

    // 字体设置说明：
    // 1. UKK TZK1 是推荐的哈萨克语字体，支持阿拉伯文和西里尔文
    // 2. 可以根据需要修改字体设置，确保系统中安装了相应的字体
    // 3. 如果系统中没有 UKK TZK1 字体，会自动回退到 sans-serif 字体
    // 输入法核心模块
    const KazakhIME = {
        // 状态管理
        state: {
            inputMode: 'english', // 'arabic', 'cyrillic' or 'english'
            keyboardVisible: false,
            keyboardShift: false,
            lastActiveInput: null
        },
        
        // 西里尔文字符映射表
        cyrillicCharMap: {
            // 小写字母映射
            'q': 'қ', 'w': 'ў', 'e': 'е', 'r': 'р', 't': 'т', 'y': 'у', 'u': 'ү', 'i': 'і', 'o': 'о', 'p': 'п',
            '[': ']', ']': '[', 'a': 'а', 's': 'с', 'd': 'д', 'f': 'ф', 'g': 'ғ', 'h': 'һ', 'j': 'ж',
            'k': 'к', 'l': 'л', ';': ';', "'": "'", 'z': 'з', 'x': 'х', 'c': 'ц', 'v': 'в', 'b': 'б', 'n': 'н',
            'm': 'м', ',': ',',
            // 大写字母映射
            'Q': 'Қ', 'W': 'Ў', 'E': 'Е', 'R': 'Р', 'T': 'Т', 'Y': 'У', 'U': 'Ү', 'I': 'І', 'O': 'О', 'P': 'П',
            '{': '}', '}': '{', 'A': 'А', 'S': 'С', 'D': 'Д', 'F': 'Ф', 'G': 'Ғ', 'H': 'Һ', 'J': 'Ж',
            'K': 'К', 'L': 'Л', ':': ':', '"': '"', 'Z': 'З', 'X': 'Х', 'C': 'Ц', 'V': 'В', 'B': 'Б', 'N': 'Н',
            'M': 'М', '<': '<', '>': '>', '?': '?'
        },
        
        // 虚拟键盘布局
        keyboardLayout: [
            // 第一行
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            // 第二行
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            // 第三行
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            // 第四行
            ['shift', 'space', 'backspace']
        ],
        
        // 字符映射表
        charMap: {
            // 小写字母映射
            'q': 'چ', 'w': 'ۋ', 'e': 'ء', 'r': 'ر', 't': 'ت', 'y': 'ي', 'u': 'ۇ', 'i': 'ڭ', 'o': 'و', 'p': 'پ',
            '[': ']', ']': '[', 'a': 'ھ', 's': 'س', 'd': 'د', 'f': 'ا', 'g': 'ە', 'h': 'ى', 'j': 'ق',
            'k': 'ك', 'l': 'ل', ';': '؛', "'": "'", 'z': 'ز', 'x': 'ش', 'c': 'ع', 'v': 'ۆ', 'b': 'ب', 'n': 'ن',
            'm': 'م', ',': '،',
            // 大写字母映射
            'Q': 'چ', 'W': 'ۋ', 'E': 'ء', 'R': 'ر', 'T': 'ت', 'Y': 'ي', 'U': 'ٷ', 'I': 'ڭ', 'O': 'ٶ', 'P': 'پ',
            '{': '}', '}': '{', 'A': 'ٵ', 'S': 'س', 'D': 'د', 'F': 'ف', 'G': 'گ', 'H': 'ح', 'J': 'ج',
            'K': 'ك', 'L': 'ل', ':': ':', '"': '"', 'Z': 'ز', 'X': 'ع', 'C': 'ۆ', 'V': 'ب', 'B': 'ن', 'N': 'م',
            'M': 'م', '<': '»', '>': '«', '?': '؟'
        },
        
        // 初始化函数
        init: function() {
            this.createStatusButton();
            this.createKeyboardToggleButton();
            this.createVirtualKeyboard();
            this.bindEvents();
            this.setupMutationObserver();
            // 初始化时更新所有现有输入元素
            this.updateInputElements();
            console.log('[KazakhIME] Loaded');
        },
        
        // 创建键盘切换按钮
        createKeyboardToggleButton: function() {
            const btn = document.createElement('button');
            btn.id = 'kazakh-ime-keyboard-toggle';
            btn.innerHTML = '⌨';
            btn.title = '显示/隐藏虚拟键盘';
            btn.style.cssText = 'position:fixed;bottom:45px;right:195px;width:20px;height:20px;border-radius:4px;background:#e0e0e0;border:2px solid #ccc;cursor:pointer;font-size:12px;z-index:9999;transition:all 0.3s;display:flex;align-items:center;justify-content:center;';
            
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleKeyboard();
            });
            
            document.body.appendChild(btn);
            return btn;
        },
        
        // 创建虚拟键盘
        createVirtualKeyboard: function() {
            const keyboard = document.createElement('div');
            keyboard.id = 'kazakh-ime-virtual-keyboard';
            keyboard.style.cssText = 'position:fixed;bottom:10px;left:50%;transform:translateX(-50%);background:#fff;border:2px solid #ccc;border-radius:8px;padding:10px;z-index:9998;display:none;box-shadow:0 4px 12px rgba(0,0,0,0.15);cursor:move;';
            
            // 创建拖动手柄
            const handle = document.createElement('div');
            handle.style.cssText = 'height:20px;background:#f5f5f5;border-radius:4px;margin-bottom:10px;cursor:grab;display:flex;align-items:center;justify-content:space-between;font-size:12px;color:#666;';
            handle.title = '拖动'; // 鼠标悬停时显示提示
            
            // 拖动emoji
            const handleText = document.createElement('span');
            handleText.textContent = '☰'; // 菜单图标emoji
            handleText.style.marginLeft = '10px';
            handle.appendChild(handleText);
            
            // 关闭按钮
            const closeBtn = document.createElement('button');
            closeBtn.className = 'kazakh-ime-key';
            closeBtn.dataset.key = 'close';
            closeBtn.innerHTML = '✕';
            closeBtn.style.cssText = 'margin:0 10px 0 0;padding:2px 6px;border:none;border-radius:4px;cursor:pointer;font-size:12px;background:#ff6b6b;color:white;';
            
            // 点击事件
            closeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleKeyboard();
            });
            
            handle.appendChild(closeBtn);
            handle.style.userSelect = 'none';
            keyboard.appendChild(handle);
            
            // 创建键盘行
            this.keyboardLayout.forEach((row, rowIndex) => {
                const rowDiv = document.createElement('div');
                rowDiv.style.cssText = 'display:flex;justify-content:center;margin-bottom:5px;';
                
                // 第一行不再显示关闭按钮
                if (rowIndex === 0) {
                    row = row.filter(key => key !== 'close');
                }
                
                row.forEach((key) => {
                    const keyBtn = this.createKeyboardKey(key);
                    rowDiv.appendChild(keyBtn);
                });
                
                keyboard.appendChild(rowDiv);
            });
            
            // 添加拖动功能
            this.setupDragAndDrop(keyboard, handle);
            
            document.body.appendChild(keyboard);
            return keyboard;
        },
        
        // 设置拖放功能
        setupDragAndDrop: function(element, handle) {
            let isDragging = false;
            let startX, startY, offsetX, offsetY;
            
            // 鼠标按下事件
            handle.addEventListener('mousedown', (e) => {
                isDragging = true;
                startX = e.clientX;
                startY = e.clientY;
                
                // 获取元素当前位置
                const rect = element.getBoundingClientRect();
                offsetX = startX - rect.left;
                offsetY = startY - rect.top;
                
                // 更改光标样式
                element.style.cursor = 'grabbing';
                handle.style.cursor = 'grabbing';
                
                e.preventDefault();
            });
            
            // 鼠标移动事件
            document.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                
                const newX = e.clientX - offsetX;
                const newY = e.clientY - offsetY;
                
                // 设置新位置，清除bottom属性避免冲突
                element.style.left = `${newX}px`;
                element.style.top = `${newY}px`;
                element.style.bottom = 'auto'; // 清除bottom属性
                element.style.transform = 'none'; // 移除translateX(-50%)
                
                e.preventDefault();
            });
            
            // 鼠标释放事件
            document.addEventListener('mouseup', () => {
                if (isDragging) {
                    isDragging = false;
                    element.style.cursor = 'move';
                    handle.style.cursor = 'grab';
                }
            });
            
            // 鼠标离开窗口事件
            document.addEventListener('mouseleave', () => {
                if (isDragging) {
                    isDragging = false;
                    element.style.cursor = 'move';
                    handle.style.cursor = 'grab';
                }
            });
        },
        
        // 创建键盘按键
        createKeyboardKey: function(key) {
            const btn = document.createElement('button');
            btn.className = 'kazakh-ime-key';
            btn.dataset.key = key;
            
            // 设置按钮样式
            let buttonStyle = 'margin:2px;padding:8px 12px;border:none;border-radius:4px;cursor:pointer;font-size:16px;min-width:36px;min-height:36px;transition:all 0.1s;background:#f5f5f5;color:#333;font-family:UKK TZK1,sans-serif;z-index:1;';
            
            if (key === 'shift') {
                btn.innerHTML = '⇧';
                buttonStyle += 'background:#ddd;font-weight:bold;min-width:60px;';
            } else if (key === 'space') {
                btn.innerHTML = ' ';
                buttonStyle += 'min-width:200px;';
            } else if (key === 'backspace') {
                btn.innerHTML = '⌫';
                buttonStyle += 'background:#ddd;font-weight:bold;min-width:60px;';
            } else if (key === 'close') {
                btn.innerHTML = '❌';
                buttonStyle += 'background:#ff6b6b;font-weight:bold;min-width:60px;color:white;';
            } else {
                let displayChar;
                if (this.state.inputMode === 'arabic') {
                    displayChar = this.charMap[key] || this.charMap[key.toUpperCase()] || key;
                } else if (this.state.inputMode === 'cyrillic') {
                    displayChar = this.cyrillicCharMap[key] || this.cyrillicCharMap[key.toUpperCase()] || key;
                } else {
                    displayChar = key;
                }
                btn.innerHTML = displayChar;
            }
            
            btn.style.cssText = buttonStyle;
            
            // 悬停效果
            btn.addEventListener('mouseenter', function() {
                this.style.background = '#e0e0e0';
                this.style.transform = 'scale(1.05)';
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.background = key === 'shift' || key === 'backspace' ? '#ddd' : '#f5f5f5';
                this.style.transform = 'scale(1)';
            });
            
            // 按下效果
            btn.addEventListener('mousedown', function(e) {
                e.stopPropagation(); // 阻止事件冒泡到键盘容器
                this.style.background = '#ccc';
                this.style.transform = 'scale(0.95)';
            });
            
            btn.addEventListener('mouseup', function(e) {
                e.stopPropagation(); // 阻止事件冒泡到键盘容器
                this.style.background = key === 'shift' || key === 'backspace' ? '#ddd' : '#f5f5f5';
                this.style.transform = 'scale(1.05)';
            });
            
            // 点击事件
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation(); // 阻止事件冒泡到键盘容器
                this.handleVirtualKeyPress(key);
            });
            
            return btn;
        },
        
        // 处理虚拟键盘按键
        handleVirtualKeyPress: function(key) {
            // 使用最后一个活动的输入元素，而不是当前的activeElement
            // 因为点击虚拟键盘时，activeElement会变成按钮
            const activeElement = this.state.lastActiveInput;
            
            if (key === 'shift') {
                this.toggleKeyboardShift();
                return;
            }
            
            if (key === 'close') {
                this.toggleKeyboard();
                return;
            }
            
            if (key === 'space') {
                if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
                    const selectionStart = activeElement.selectionStart;
                    const selectionEnd = activeElement.selectionEnd;
                    const value = activeElement.value;
                    activeElement.value = value.substring(0, selectionStart) + ' ' + value.substring(selectionEnd);
                    activeElement.selectionStart = activeElement.selectionEnd = selectionStart + 1;
                    activeElement.dispatchEvent(new Event('input', { bubbles: true }));
                }
                return;
            }
            
            if (key === 'backspace') {
                if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
                    const selectionStart = activeElement.selectionStart;
                    const selectionEnd = activeElement.selectionEnd;
                    const value = activeElement.value;
                    
                    if (selectionStart === selectionEnd && selectionStart > 0) {
                        activeElement.value = value.substring(0, selectionStart - 1) + value.substring(selectionEnd);
                        activeElement.selectionStart = activeElement.selectionEnd = selectionStart - 1;
                    } else if (selectionStart !== selectionEnd) {
                        activeElement.value = value.substring(0, selectionStart) + value.substring(selectionEnd);
                        activeElement.selectionStart = activeElement.selectionEnd = selectionStart;
                    }
                    
                    activeElement.dispatchEvent(new Event('input', { bubbles: true }));
                }
                return;
            }
            
            // 处理普通字符
            if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
                const charKey = this.state.keyboardShift ? key.toUpperCase() : key;
                let mappedChar;
                
                if (this.state.inputMode === 'arabic') {
                    mappedChar = this.charMap[charKey] || this.charMap[key] || charKey;
                } else if (this.state.inputMode === 'cyrillic') {
                    mappedChar = this.cyrillicCharMap[charKey] || this.cyrillicCharMap[key] || charKey;
                } else {
                    mappedChar = charKey;
                }
                
                const selectionStart = activeElement.selectionStart;
                const selectionEnd = activeElement.selectionEnd;
                const value = activeElement.value;
                
                activeElement.value = value.substring(0, selectionStart) + mappedChar + value.substring(selectionEnd);
                activeElement.selectionStart = activeElement.selectionEnd = selectionStart + mappedChar.length;
                activeElement.dispatchEvent(new Event('input', { bubbles: true }));
            }
        },
        
        // 切换键盘显示
        toggleKeyboard: function() {
            this.state.keyboardVisible = !this.state.keyboardVisible;
            const keyboard = document.getElementById('kazakh-ime-virtual-keyboard');
            const toggleBtn = document.getElementById('kazakh-ime-keyboard-toggle');
            
            if (keyboard) {
                keyboard.style.display = this.state.keyboardVisible ? 'block' : 'none';
            }
            
            if (toggleBtn) {
                toggleBtn.style.background = this.state.keyboardVisible ? 'linear-gradient(135deg,#f093fb 0%,#f5576c 100%)' : '#e0e0e0';
                toggleBtn.style.color = this.state.keyboardVisible ? 'white' : '#333';
                toggleBtn.style.borderColor = this.state.keyboardVisible ? '#f5576c' : '#ccc';
            }
        },
        
        // 切换Shift状态
        toggleKeyboardShift: function() {
            this.state.keyboardShift = !this.state.keyboardShift;
            this.updateVirtualKeyboardDisplay();
        },
        
        // 设置 MutationObserver 监听动态添加的输入元素
        setupMutationObserver: function() {
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) { // 元素节点
                            // 检查是否是输入元素
                            if ((node.tagName === 'INPUT' && node.type === 'text') || 
                                node.tagName === 'TEXTAREA') {
                                this.updateInputElement(node);
                            }
                            // 检查子元素中是否有输入元素
                            const inputs = node.querySelectorAll ? 
                                node.querySelectorAll('input[type="text"], textarea') : [];
                            inputs.forEach((el) => this.updateInputElement(el));
                        }
                    });
                });
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        },
        
        // 绑定事件
        bindEvents: function() {
            // 使用事件委托，减少事件监听器数量
            document.addEventListener('keydown', this.handleKeyDown.bind(this));
            
            // 监听输入元素的focus事件，记录最后一个活动的输入元素
            document.addEventListener('focusin', (e) => {
                if (e.target.tagName === 'INPUT' && e.target.type === 'text' || 
                    e.target.tagName === 'TEXTAREA') {
                    this.state.lastActiveInput = e.target;
                }
            });
        },
        
        // 处理键盘事件
        handleKeyDown: function(e) {
            // 处理快捷键切换模式
            if (e.ctrlKey && e.shiftKey && e.key === 'K') {
                e.preventDefault();
                this.toggleInputMode();
                return;
            }
            
            // 释放除了Shift键之外的所有组合键给系统处理
            // Shift键需要保留，用于大写字母映射
            if (e.ctrlKey || e.altKey || e.metaKey) {
                return;
            }
            
            // 忽略回车键、退格键、删除键、Tab键等功能键，让浏览器正常处理
            const functionKeys = ['Enter', 'Backspace', 'Delete', 'Tab', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'];
            if (functionKeys.includes(e.key)) {
                return;
            }
            
            // 处理字符映射
            if (this.state.inputMode === 'arabic' && this.charMap[e.key]) {
                e.preventDefault();
                this.handleCharacterInput(e);
            } else if (this.state.inputMode === 'cyrillic' && this.cyrillicCharMap[e.key]) {
                e.preventDefault();
                this.handleCharacterInput(e);
            }
        },
        
        // 切换输入模式
        toggleInputMode: function() {
            // 循环切换：english → arabic → cyrillic → english
            if (this.state.inputMode === 'english') {
                this.state.inputMode = 'arabic';
                console.log('[KazakhIME] Arabic Mode');
            } else if (this.state.inputMode === 'arabic') {
                this.state.inputMode = 'cyrillic';
                console.log('[KazakhIME] Cyrillic Mode');
            } else {
                this.state.inputMode = 'english';
                console.log('[KazakhIME] English Mode');
            }
            // 更新所有输入元素
            this.updateInputElements();
            this.updateStatusButton();
        },
        
        // 更新当前活动的输入元素
        updateActiveInputElement: function() {
            const activeElement = document.activeElement;
            if (activeElement && 
                (activeElement.tagName === 'INPUT' && activeElement.type === 'text' || 
                 activeElement.tagName === 'TEXTAREA')) {
                this.updateInputElement(activeElement);
            }
        },
        
        // 处理字符输入
        handleCharacterInput: function(e) {
            const target = e.target;
            if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
                const selectionStart = target.selectionStart;
                const selectionEnd = target.selectionEnd;
                const value = target.value;
                
                // 根据当前模式获取映射字符
                let mappedChar;
                if (this.state.inputMode === 'arabic') {
                    mappedChar = this.charMap[e.key];
                } else if (this.state.inputMode === 'cyrillic') {
                    mappedChar = this.cyrillicCharMap[e.key];
                }
                
                if (mappedChar) {
                    // 插入映射字符
                    target.value = value.substring(0, selectionStart) + mappedChar + value.substring(selectionEnd);
                    
                    // 更新光标位置
                    target.selectionStart = target.selectionEnd = selectionStart + mappedChar.length;
                    
                    // 触发输入事件，确保表单验证等功能正常
                    target.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
        },
        
        // 更新输入元素
        updateInputElements: function() {
            const inputs = document.querySelectorAll('input[type="text"], textarea');
            inputs.forEach((el) => {
                this.updateInputElement(el);
            });
        },
        
        // 更新单个输入元素
        updateInputElement: function(el) {
            if (this.state.inputMode === 'arabic') {
                this.setArabicMode(el);
            } else if (this.state.inputMode === 'cyrillic') {
                this.setCyrillicMode(el);
            } else {
                this.setEnglishMode(el);
            }
        },
        
        // 设置阿拉伯文模式
        setArabicMode: function(el) {
            el.style.direction = 'rtl';
            el.style.fontFamily = FONT_SETTINGS.arabic;
            el.setAttribute('lang', 'en-US');
            el.setAttribute('inputmode', 'latin');
            el.setAttribute('dir', 'rtl');
            el.setAttribute('autocomplete', 'off');
        },
        
        // 设置西里尔文模式
        setCyrillicMode: function(el) {
            el.style.direction = 'ltr';
            el.style.fontFamily = FONT_SETTINGS.cyrillic;
            el.setAttribute('lang', 'kk');
            el.setAttribute('inputmode', 'latin');
            el.setAttribute('dir', 'ltr');
            el.setAttribute('autocomplete', 'off');
        },
        
        // 设置英文模式
        setEnglishMode: function(el) {
            el.style.direction = 'ltr';
            el.style.fontFamily = FONT_SETTINGS.english;
            el.setAttribute('lang', 'zh-CN');
            el.setAttribute('inputmode', 'text');
            el.setAttribute('dir', 'ltr');
            el.setAttribute('autocomplete', 'on');
        },
        
        // 设置光标位置
        setCursorPosition: function(el) {
            setTimeout(() => {
                try {
                    el.focus();
                    const endPos = el.value.length;
                    el.setSelectionRange(endPos, endPos);
                    
                    // 兼容IE
                    if (typeof el.createTextRange !== 'undefined') {
                        const range = el.createTextRange();
                        range.collapse(true);
                        range.select();
                    }
                } catch (e) {
                    console.log('Error setting cursor position:', e);
                }
            }, 300);
        },
        
        // 创建状态按钮
        createStatusButton: function() {
            const btn = document.createElement('button');
            btn.id = 'kazakh-ime-status';
            btn.textContent = 'قا';
            btn.title = '(Ctrl+Shift+K قازاقشا)';
            btn.style.cssText = 'position:fixed;bottom:45px;right:170px;width:20px;height:20px;border-radius:4px;background:#e0e0e0;border:2px solid #ccc;cursor:pointer;font-weight:bold;font-size:12px;padding-left:2px;z-index:9999;transition:all 0.3s;';
            
            // 绑定点击事件
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleInputMode();
            });
            
            document.body.appendChild(btn);
            return btn;
        },
        
        // 更新状态按钮
        updateStatusButton: function() {
            const btn = document.getElementById('kazakh-ime-status');
            if (!btn) {
                this.createStatusButton();
                return;
            }
            
            if (this.state.inputMode === 'arabic') {
                btn.style.background = 'linear-gradient(135deg,#f093fb 0%,#f5576c 100%)';
                btn.style.color = 'white';
                btn.style.borderColor = '#f5576c';
                btn.textContent = 'قا';
            } else if (this.state.inputMode === 'cyrillic') {
                btn.style.background = 'linear-gradient(135deg,#4facfe 0%,#00f2fe 100%)';
                btn.style.color = 'white';
                btn.style.borderColor = '#00f2fe';
                btn.textContent = 'қ';
            } else {
                btn.style.background = '#e0e0e0';
                btn.style.color = '#333';
                btn.style.borderColor = '#ccc';
                btn.textContent = 'قا';
            }
            
            // 更新虚拟键盘按键显示
            this.updateVirtualKeyboardDisplay();
        },
        
        // 更新虚拟键盘按键显示
        updateVirtualKeyboardDisplay: function() {
            const keyboard = document.getElementById('kazakh-ime-virtual-keyboard');
            if (!keyboard) return;
            
            const keys = keyboard.querySelectorAll('.kazakh-ime-key');
            keys.forEach((key) => {
                const keyValue = key.dataset.key;
                
                if (keyValue === 'shift') {
                    // 更新Shift按钮状态
                    key.style.background = this.state.keyboardShift ? 'linear-gradient(135deg,#f093fb 0%,#f5576c 100%)' : '#ddd';
                    key.style.color = this.state.keyboardShift ? 'white' : '#333';
                } else if (keyValue === 'close') {
                    // 保持关闭按钮显示
                    key.innerHTML = '✕';
                } else if (keyValue !== 'space' && keyValue !== 'backspace') {
                    // 处理普通字符
                    const displayKey = this.state.keyboardShift ? keyValue.toUpperCase() : keyValue;
                    let displayChar;
                    
                    if (this.state.inputMode === 'arabic') {
                        displayChar = this.charMap[displayKey] || this.charMap[keyValue] || displayKey;
                    } else if (this.state.inputMode === 'cyrillic') {
                        displayChar = this.cyrillicCharMap[displayKey] || this.cyrillicCharMap[keyValue] || displayKey;
                    } else {
                        displayChar = displayKey;
                    }
                    key.innerHTML = displayChar;
                }
            });
        }
    };
    
    // 初始化输入法
    KazakhIME.init();
 })();