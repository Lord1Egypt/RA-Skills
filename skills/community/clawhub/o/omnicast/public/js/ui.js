export const log = (msg) => {
    const box = document.getElementById('terminal-log');
    if (box) { box.innerHTML += `<div>${msg}</div>`; box.scrollTop = box.scrollHeight; }
};

export const setApiLoading = (show) => { 
    document.getElementById('log-active-spinner').style.display = show ? 'block' : 'none'; 
};

export const updateLoadingMessage = (msg) => {
    const el = document.querySelector('#log-active-spinner em');
    if (el) el.textContent = msg;
};

export const displayThumbnail = (url, promptText) => {
    document.getElementById('podcast-cover-image').src = `${url}?t=${Date.now()}`;
    if(promptText) document.getElementById('generated-image-prompt').innerText = promptText;
    document.getElementById('thumbnail-display').style.display = 'block';
};

export const resetWorkspace = () => {
    document.getElementById('script-editor').value = '';
    document.getElementById('audio-container').style.display = 'none';
    document.getElementById('thumbnail-display').style.display = 'none';
    
    // Clear the prompt text, but leave the editor visible
    document.getElementById('image-prompt-input').value = ''; 
    
    document.getElementById('linkedin-display').style.display = 'none';
    document.getElementById('live-captions').innerHTML = '';
    
    document.getElementById('sourceUrl').value = '';
    document.getElementById('sourceFile').value = '';
    
    document.getElementById('word-count').innerText = '0';
    document.getElementById('est-time').innerText = '0:00';
    document.getElementById('linkedin-warning').style.display = 'none';
};

export const showSessionControls = () => { 
    // Intentionally left blank as the HTML element does not exist
};

export const buildLiveCaptions = (vttText) => {
    const container = document.getElementById('live-captions');
    container.innerHTML = ''; 

    try {
        if (!vttText || !vttText.includes('-->')) throw new Error("Invalid VTT structure detected.");

        const regex = /(\d{2}:\d{2}:\d{2}\.\d{3})\s-->\s(\d{2}:\d{2}:\d{2}\.\d{3})\n<v\s([^>]+)>(.*?)\n/g;
        let match;
        const timeToSeconds = (timeStr) => {
            const [h, m, s] = timeStr.split(':');
            return parseInt(h) * 3600 + parseInt(m) * 60 + parseFloat(s);
        };

        while ((match = regex.exec(vttText)) !== null) {
            const startSec = timeToSeconds(match[1]);
            const endSec = timeToSeconds(match[2]);
            const speaker = match[3];
            const text = match[4];

            const lineDiv = document.createElement('div');
            lineDiv.className = 'caption-line';
            lineDiv.dataset.start = startSec;
            lineDiv.dataset.end = endSec;
            lineDiv.innerHTML = `<strong style="color: #3498db;">${speaker}:</strong> <span>${text}</span>`;
            
            lineDiv.addEventListener('click', () => {
                const audio = document.getElementById('podcast-audio');
                audio.currentTime = startSec;
                audio.play();
            });

            container.appendChild(lineDiv);
        }

        if (container.children.length === 0) throw new Error("No valid captions matched the regex.");

    } catch (err) {
        console.warn("VTT Error Boundary Triggered:", err);
        container.innerHTML = `
            <div style="padding: 20px; color: #e74c3c; text-align: center; font-family: sans-serif;">
                ⚠️ <strong>Live Captions Unavailable</strong><br>
                <span style="font-size: 0.9em; opacity: 0.8;">The transcript format returned is unsupported. Audio will still play normally.</span>
            </div>
        `;
    }
};

export const syncCaptionsWithAudio = (currentTime) => {
    const lines = document.querySelectorAll('.caption-line');
    let activeLineFound = false;
    lines.forEach(line => {
        const start = parseFloat(line.dataset.start);
        const end = parseFloat(line.dataset.end);
        
        if (currentTime >= start && currentTime <= end) {
            line.style.opacity = '1';
            line.style.color = '#2ecc71'; 
            if (!activeLineFound) {
                line.scrollIntoView({ behavior: 'smooth', block: 'center' });
                activeLineFound = true;
            }
        } else {
            line.style.opacity = '0.4';
            line.style.color = '#bdc3c7';
        }
    });
};