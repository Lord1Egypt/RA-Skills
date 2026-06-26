import { log, setApiLoading, updateLoadingMessage, displayThumbnail, resetWorkspace, showSessionControls, buildLiveCaptions, syncCaptionsWithAudio } from './ui.js';
import { requestSessionCleanup } from './api.js';

let currentVideoId = `session_${Date.now()}`;

const saveEditedFile = async (type, content, btnElement) => {
    try {
        const res = await fetch('/api/save-file', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, type, content })
        });
        if (!res.ok) throw new Error("Failed to save.");
        btnElement.innerText = "✅ Saved!";
        setTimeout(() => { btnElement.innerText = "💾 Save " + (type==='linkedin'?'Post':type.charAt(0).toUpperCase() + type.slice(1)); }, 2000);
    } catch(err) { alert(err.message); }
};

document.getElementById('btn-save-script').addEventListener('click', (e) => saveEditedFile('script', document.getElementById('script-editor').value, e.target));
document.getElementById('btn-save-prompt').addEventListener('click', (e) => saveEditedFile('prompt', document.getElementById('image-prompt-input').value, e.target));
document.getElementById('btn-save-linkedin').addEventListener('click', (e) => saveEditedFile('linkedin', document.getElementById('linkedin-post-text').value, e.target));

document.getElementById('btn-ingest').addEventListener('click', async () => {
    const url = document.getElementById('sourceUrl').value;
    const file = document.getElementById('sourceFile').files[0];
    if (!url && !file) return alert("Please enter a URL or select a file.");
    
    setApiLoading(true); showSessionControls();
    log("Initiating media ingestion..."); updateLoadingMessage("Extracting text...");
    
    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };
    
    const formData = new FormData();
    formData.append('id', currentVideoId);
    if (file) formData.append('file', file);
    else { formData.append('sourceType', 'url'); formData.append('url', url); }
    
    try {
        const res = await fetch('/api/ingest', { method: 'POST', body: formData });
        const data = await res.json();
        if(data.success) {
            document.getElementById('original-text-section').style.display = 'block';
            document.getElementById('original-text-viewer').value = data.fullText;
            fetchSessions(); // Refresh sessions list in case it's new
        }
    } catch (e) { log(`❌ ${e.message}`); }
    
    eventSource.close(); setApiLoading(false);
});

document.getElementById('btn-translate-original').addEventListener('click', async () => {
    const targetLang = document.getElementById('viewLanguage').value;
    const viewer = document.getElementById('original-text-viewer');
    viewer.value = "Translating... please wait.";
    try {
        const res = await fetch('/api/translate-original', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, targetLanguage: targetLang })
        });
        const data = await res.json();
        viewer.value = data.text;
    } catch(err) { viewer.value = "Translation failed."; }
});

const updateScriptStats = () => {
    const text = document.getElementById('script-editor').value;
    const wordCount = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
    document.getElementById('word-count').innerText = wordCount;
    document.getElementById('est-time').innerText = `${Math.floor(Math.round((wordCount / 150) * 60) / 60)}:${(Math.round((wordCount / 150) * 60) % 60).toString().padStart(2, '0')}`;
    document.getElementById('linkedin-warning').style.display = (wordCount > 0 && (wordCount < 450 || wordCount > 2100)) ? 'inline' : 'none';
};

document.getElementById('script-editor').addEventListener('input', () => {
    updateScriptStats();
    document.getElementById('btn-save-script').style.display = 'block';
});
document.getElementById('image-prompt-input').addEventListener('input', () => {
    document.getElementById('btn-save-prompt').style.display = 'block';
});
document.getElementById('linkedin-post-text').addEventListener('input', () => {
    document.getElementById('btn-save-linkedin').style.display = 'block';
});

document.getElementById('btn-draft').addEventListener('click', async () => {
    setApiLoading(true); log("Initiating Gemini script drafting..."); updateLoadingMessage("Drafting...");
    const host1 = document.getElementById('host1').value || 'Alex', host2 = document.getElementById('host2').value || 'Sam', language = document.getElementById('targetLanguage').value;

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/draft-script', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, host1, host2, targetLanguage: language })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);
        document.getElementById('script-editor').value = data.script;
        updateScriptStats();
        document.getElementById('btn-save-script').style.display = 'block';
    } catch (e) { log(`❌ ${e.message}`); }
    eventSource.close(); setApiLoading(false);
});

document.getElementById('btn-generate-audio').addEventListener('click', async () => {
    setApiLoading(true);
    log("Initiating audio synthesis pipeline...");
    updateLoadingMessage("Synthesizing...");
    
    const script = document.getElementById('script-editor').value;
    const host1 = document.getElementById('host1').value || 'Alex';
    const host2 = document.getElementById('host2').value || 'Sam';

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    
    eventSource.onmessage = async (e) => {
        const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message);
        
        if (d.status === 'done') {
            eventSource.close(); setApiLoading(false);
            const audio = document.getElementById('podcast-audio');
            const audioUrl = `/downloads/${currentVideoId}/podcast.m4a`;
            const vttUrl = `/downloads/${currentVideoId}/podcast.vtt`;
            
            audio.src = audioUrl;
            document.getElementById('podcast-vtt').src = vttUrl;
            document.getElementById('audio-container').style.display = 'block';

            try {
                const vttRes = await fetch(vttUrl);
                buildLiveCaptions(await vttRes.text());
            } catch (err) { console.error("Failed to load VTT for UI", err); }
        }
    };

    try {
        await fetch('/api/synthesize', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, script, host1, host2 })
        });
    } catch(e) { log(`❌ ${e.message}`); eventSource.close(); setApiLoading(false); }
});

document.getElementById('podcast-audio').addEventListener('timeupdate', (e) => {
    syncCaptionsWithAudio(e.target.currentTime);
});

document.getElementById('btn-draft-prompt').addEventListener('click', async () => {
    setApiLoading(true);
    log("Analyzing script for visual concepts...");
    updateLoadingMessage("Designing...");
    
    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/draft-image-prompt', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);

        document.getElementById('image-prompt-input').value = data.prompt;
        document.getElementById('prompt-editor-section').style.display = 'block';
    } catch (e) { log(`❌ ${e.message}`); }
    
    eventSource.close(); setApiLoading(false);
});

document.getElementById('btn-generate-thumbnail').addEventListener('click', async () => {
    setApiLoading(true);
    const userPrompt = document.getElementById('image-prompt-input').value;
    if (!userPrompt) return alert("Please draft or enter a prompt first.");

    log("Sending render request to Gemini 3.1 Flash Image...");
    updateLoadingMessage("Rendering...");

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/generate-thumbnail', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, prompt: userPrompt })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);

        displayThumbnail(`/downloads/${currentVideoId}/${data.file}`, ""); 
        updateLoadingMessage("Done!");
    } catch (e) { log(`❌ ${e.message}`); updateLoadingMessage("Error!"); }
    
    eventSource.close(); setApiLoading(false);
});

document.getElementById('btn-generate-linkedin').addEventListener('click', async () => {
    setApiLoading(true);
    const btn = document.getElementById('btn-generate-linkedin');
    btn.disabled = true;
    
    const selectedLangs = Array.from(document.querySelectorAll('input[name="vtt-lang"]:checked'))
                               .map(cb => cb.value);
    
    log(selectedLangs.length > 0 
        ? `Initiating LinkedIn packaging & translating VTT to ${selectedLangs.length} languages...`
        : "Initiating LinkedIn video packaging...");
    updateLoadingMessage("Packaging...");

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/generate-linkedin', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentVideoId, targetCaptionLanguages: selectedLangs })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Failed to generate LinkedIn package.");

        document.getElementById('linkedin-post-text').value = data.post;
        document.getElementById('linkedin-video-player').src = `/downloads/${currentVideoId}/${data.video}?t=${Date.now()}`;
        document.getElementById('linkedin-display').style.display = 'block';
    } catch (e) { log(`❌ ${e.message}`); alert(e.message); } 
    finally { eventSource.close(); setApiLoading(false); btn.disabled = false; }
});

let youtubeAccessToken = null;
let tokenClient;

window.onload = async () => {
    try {
        const configRes = await fetch('/api/config');
        const config = await configRes.json();

        if (config.googleClientId) {
            tokenClient = google.accounts.oauth2.initTokenClient({
                client_id: config.googleClientId, 
                scope: 'https://www.googleapis.com/auth/youtube.upload',
                callback: (tokenResponse) => {
                    if (tokenResponse && tokenResponse.access_token) {
                        youtubeAccessToken = tokenResponse.access_token;
                        document.getElementById('youtube-auth-status').innerText = '✅ Authenticated';
                        document.getElementById('youtube-auth-status').style.color = '#fff';
                        document.getElementById('btn-youtube-login').style.display = 'none';
                        document.getElementById('youtube-upload-controls').style.display = 'block';
                    }
                },
            });
        }
    } catch (err) { console.error("Failed to load config:", err); }
};

document.getElementById('btn-youtube-login').addEventListener('click', () => {
    if (tokenClient) { tokenClient.requestAccessToken(); } 
    else { alert("Client ID missing from .env configuration."); }
});

document.getElementById('btn-upload-youtube').addEventListener('click', async () => {
    if (!youtubeAccessToken) return alert("Please sign in with Google first.");
    
    const title = document.getElementById('youtube-title').value;
    const description = document.getElementById('youtube-description').value;
    
    if (!title) return alert("Please provide a title for the YouTube video.");

    setApiLoading(true);
    const btn = document.getElementById('btn-upload-youtube');
    btn.disabled = true;
    
    log("Connecting to YouTube API...");
    updateLoadingMessage("Uploading...");

    const eventSource = new EventSource(`/api/stream-logs?id=${currentVideoId}`);
    await new Promise(resolve => { eventSource.onopen = resolve; setTimeout(resolve, 500); });
    eventSource.onmessage = e => { const d = JSON.parse(e.data); log(d.message); updateLoadingMessage(d.message); };

    try {
        const res = await fetch('/api/upload-youtube', {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                id: currentVideoId,
                title: title,
                description: description,
                accessToken: youtubeAccessToken 
            })
        });
        
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Failed to upload to YouTube.");

        log(`✅ Successfully uploaded! YouTube Video ID: ${data.videoId}`);
        alert(`Upload complete! Video ID: ${data.videoId}\nIt is currently set to Private.`);
        
    } catch (e) { 
        log(`❌ ${e.message}`); 
        alert(e.message); 
    } finally { 
        eventSource.close(); 
        setApiLoading(false); 
        btn.disabled = false; 
    }
});

// --- SESSION MANAGEMENT LOGIC ---

const fetchSessions = async () => {
    try {
        const res = await fetch('/api/sessions');
        const data = await res.json();
        const select = document.getElementById('session-select');
        
        const currentVal = select.value;
        
        select.innerHTML = '<option value="">-- Start a New Session --</option>';
        data.sessions.forEach(session => {
            const option = document.createElement('option');
            option.value = session;
            option.innerText = session;
            select.appendChild(option);
        });
        
        if (currentVal && data.sessions.includes(currentVal)) {
            select.value = currentVal;
        }
    } catch (err) { console.error("Failed to load sessions:", err); }
};

fetchSessions();

document.getElementById('btn-load-session').addEventListener('click', async () => {
    const selectedSession = document.getElementById('session-select').value;
    
    if (!selectedSession) {
        currentVideoId = `session_${Date.now()}`;
        document.getElementById('current-session-label').innerText = "Active: New Session";
        resetWorkspace();
        return; 
    }
    
    currentVideoId = selectedSession;
    document.getElementById('current-session-label').innerText = `Active: ${currentVideoId}`;
    
    try {
        const res = await fetch(`/api/session-data?id=${currentVideoId}`);
        const data = await res.json();
        
        if (data.originalText) {
            document.getElementById('original-text-section').style.display = 'block';
            document.getElementById('original-text-viewer').value = data.originalText;
        } else {
            document.getElementById('original-text-section').style.display = 'none';
        }
        
        if (data.script) {
            document.getElementById('script-editor').value = data.script;
            updateScriptStats(); 
        } else { 
            document.getElementById('script-editor').value = ""; 
        }
        
        if (data.prompt) {
            document.getElementById('prompt-editor-section').style.display = 'block';
            document.getElementById('image-prompt-input').value = data.prompt;
        } else {
            document.getElementById('image-prompt-input').value = "";
        }
        
        if (data.linkedinPost) {
            document.getElementById('linkedin-display').style.display = 'block';
            document.getElementById('linkedin-post-text').value = data.linkedinPost;
        } else {
            document.getElementById('linkedin-post-text').value = "";
        }
        
        if (data.hasAudio) {
            document.getElementById('audio-container').style.display = 'block';
            document.getElementById('podcast-audio').src = `/downloads/${currentVideoId}/podcast.m4a`;
            document.getElementById('podcast-vtt').src = `/downloads/${currentVideoId}/podcast.vtt`;
            
            try {
                const vttRes = await fetch(`/downloads/${currentVideoId}/podcast.vtt`);
                buildLiveCaptions(await vttRes.text());
            } catch (err) { console.error("Could not load VTT", err); }
            
        } else {
            document.getElementById('audio-container').style.display = 'none';
        }
        
        if (data.hasImage) {
            displayThumbnail(`/downloads/${currentVideoId}/thumbnail.png`, "");
        } else {
            document.getElementById('thumbnail-display').style.display = 'none';
        }

        if (data.hasVideo) {
            document.getElementById('linkedin-video-player').src = `/downloads/${currentVideoId}/linkedin_podcast.mp4`;
        } else {
            document.getElementById('linkedin-video-player').src = "";
        }

        alert(`Session loaded: ${currentVideoId}`);
    } catch (err) { 
        alert("Failed to load session data."); 
    }
});

document.getElementById('btn-delete-session').addEventListener('click', async () => {
    const sessionToDelete = document.getElementById('session-select').value || currentVideoId;
    if (!sessionToDelete || sessionToDelete === `session_${Date.now()}`) return alert("No saved session selected to delete.");
    
    if (!confirm(`Are you sure you want to permanently delete data for ${sessionToDelete}?`)) return;
    
    await requestSessionCleanup(sessionToDelete);
    
    currentVideoId = `session_${Date.now()}`;
    document.getElementById('current-session-label').innerText = "Active: New Session";
    resetWorkspace();
    fetchSessions(); 
});

document.getElementById('btn-clear-all-sessions').addEventListener('click', async () => {
    if (!confirm("☢️ WARNING: This will permanently delete ALL session folders in your downloads directory. This cannot be undone. Proceed?")) return;
    
    try {
        await fetch('/api/delete-all-sessions', { method: 'DELETE' });
        
        currentVideoId = `session_${Date.now()}`;
        document.getElementById('current-session-label').innerText = "Active: New Session";
        resetWorkspace();
        fetchSessions();
        alert("All sessions have been cleared.");
    } catch(err) { 
        alert("Failed to clear sessions."); 
    }
});