import WfSettings from "/assets/v3/settings/workflow.js";
import CfgSettings from "/assets/v3/settings/config.js";
import SchSettings from "/assets/v3/settings/schedule.js";
import ConfirmDialog from "/assets/v3/components/confirm_dialog.js"
import AlertDialog from "/assets/v3/components/alert_dialog.js"

//简易的用户&群组管理
export default {
inject:['ibf'],
components:{
    "wfsettings":WfSettings,
    "cfgsettings":CfgSettings,
    "schsettings":SchSettings,
    "alert-dialog":AlertDialog,
    "confirm-dialog":ConfirmDialog
},
data() {return {
    service:{label:'',value:''},
    flow:{},
    cfg:{},
    sch:{},
    confirmDlg:null,
    alertDlg:null,
    tags:this.ibf.tags,
    serviceOpts:[]
}},
created(){
    this.serviceOpts=[
        {label:this.tags.crm.title,value:'icrm'},
        {label:this.tags.hr.title,value:'ihr'},
        {label:this.tags.busi.title,value:'ibusiness'},
        {label:this.tags.resource.title,value:'iresource'}
    ];
    this.service=this.serviceOpts[0];
},
mounted(){//不能在created中赋值，更不能在data中
    this.confirmDlg=this.$refs.confirmDlg;
    this.alertDlg=this.$refs.errMsg;
},
methods:{
back() {
    if(!this.flow.changed&&!this.cfg.changed) {
        this.ibf.back();
        return;
    }
    this.$refs.confirmDlg.show(this.tags.cfgTags.changeNotSaved,()=>{
        this.ibf.back();
    })
},
save_flow() {
    this.$refs.wfSet.save();
},
save_cfg(){
    this.$refs.cfgSet.save();
}
},
template:`
<q-layout view="hHh lpr fFf">
 <q-header>
  <q-toolbar>
   <q-btn flat round icon="arrow_back" dense @click="back"></q-btn>
   <q-toolbar-title>{{tags.settings}}</q-toolbar-title>
   <q-btn flat dense icon="list" :label="service.label">
    <q-menu>
     <q-list style="min-width:100px">
      <q-item clickable v-close-popup v-for="s in serviceOpts" @click="service=s">
       <q-item-section>{{s.label}}</q-item-section>
      </q-item>
     </q-list>
    </q-menu>
   </q-btn>
  </q-toolbar>
 </q-header>
  <q-page-container>
    <q-page class="q-pa-none">
<div v-show="flow.size>0">
 <q-banner inline-actions class="bg-indigo-1 q-ma-none" dense>
  {{tags.flowDef}}
  <template  v-slot:action>
   <q-btn icon="save" @click.stop="save_flow" class="cursor-pointer"
    :disable="!flow.changed" color="primary" flat dense></q-btn>
  </template>
 </q-banner>
 <div class="q-pa-md">
  <wfsettings v-model="flow" ref="wfSet" class="q-pa-md"
  :confirmDlg="confirmDlg" :alertDlg="alertDlg"
  :service="service.value" :flowTags="tags.flowTags"></wfsettings>
 </div>
</div>

<div v-show="cfg.size>0">
 <q-banner inline-actions class="bg-indigo-1 q-ma-none" dense>
   {{tags.cfgDef}}
   <template  v-slot:action>
    <q-btn icon="save" @click.stop="save_cfg" class="cursor-pointer"
     :disable="!cfg.changed" color="primary" flat dense></q-btn>
   </template>
 </q-banner>
 <div class="q-pa-md">
  <cfgsettings v-model="cfg" ref="cfgSet" class="q-pa-md"
  :confirmDlg="confirmDlg" :alertDlg="alertDlg"
  :service="service.value" :cfgTags="tags.cfgTags"></cfgsettings>
 </div>
</div>

<div v-show="sch.size>0">
 <q-banner inline-actions class="bg-indigo-1 q-ma-none" dense>
   {{tags.schDef}}
 </q-banner>
 <div class="q-pa-md">
  <schsettings v-model="sch" ref="schSet" class="q-pa-md" :alertDlg="alertDlg"
  :service="service.value" :cfgTags="tags.schTags"></schsettings>
 </div>
</div>

  </q-page>
 </q-page-container>
</q-layout>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
<confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></confirm-dialog>
`
}