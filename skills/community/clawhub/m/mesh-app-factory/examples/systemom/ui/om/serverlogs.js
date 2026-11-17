export default {
inject:['service', 'tags'],
data(){return {
    logs:[],
    dlList:[],
    dlState:{dlg:false, progressing:true}    
}},
created() {
    this.listLogs();
},
methods:{
listLogs() {
    var opts={method:"GET", url:"/api/listlogs"};
    this.service.request_private(opts, 'backend').then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            this.logs=[];
            return;
        }
        this.logs=resp.data.list;
    });
},
dl(f){
    var fn=f.replaceAll('/', '_');
    var token=this.service.getToken('backend');
    var hh={access_token:token,cid:Companies.curCompanyId()};
    var url='/downloadlog?n=' + encodeURIComponent(f);
    this.dlState.dlg=true;
    this.dlState.progressing=true;
    download({private:false, file:true, file_name:fn, headers:hh, url:url, timeout:30000}, 'backend').then(resp => {
        if(resp.code == RetCode.OK) {
            this.dlList.splice(0,0,{file:resp.data.saveAs,size:resp.data.size,bg:'#00000000'})
        } else {
            this.dlList.splice(0,0,{file:f,size:0,bg:'#884444'})
        }
        this.dlState.progressing=false;
    });
}
},

template: `
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
    <q-toolbar>
      <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
      <q-toolbar-title>{{tags.om.serverlogs}}</q-toolbar-title>
    </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">  
<q-list class="q-pa-md">
  <q-item v-for="l in logs" clickable class="text-primary">
   <q-item-section @click="dl(l)">{{l}}</q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs"
 :close="tags.close" ref="errDlg"></component-alert-dialog>
 
<q-dialog v-model="dlState.dlg">
<q-card style="min-width:60vw;max-width:90vw">
<q-linear-progress indeterminate rounded color="pink"
class="q-mt-sm" v-show="dlState.progressing"></q-linear-progress>
<q-card-section class="row items-center q-pb-none">
  <div class="text-h6">{{tags.om.dlList}}</div>
  <q-space></q-space>
  <q-btn icon="close" flat round dense v-close-popup></q-btn>
</q-card-section>
<q-card-section>
 <q-markup-table style="width:100%;" flat>
  <tr v-for="l in dlList" :style="{'background-color':l.bg}">
   <td>{{l.file}}</td>
   <td>{{l.size}}</td>
  </tr>
 </q-markup-table>
</q-card-section>
</q-card>
</q-dialog>
`
}