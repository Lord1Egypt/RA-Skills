export const requestThumbnail = async (id) => {
    const res = await fetch('/api/generate-thumbnail', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
    });
    return res.json();
};

export const requestSessionCleanup = async (id) => {
    await fetch('/api/delete-folder', { 
        method: 'DELETE', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id }) 
    });
};